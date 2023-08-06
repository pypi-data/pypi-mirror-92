#include "teca_metadata.h"
#include "teca_mpi.h"
#include "teca_mpi_manager.h"
#include "teca_system_interface.h"
#include "teca_mpi.h"

#include <vector>
#include <set>
#include <string>
#include <iostream>



struct file_mapper
{
    file_mapper() : index_initializer_key("num_time_steps"),
        index_request_key("time_step"), start_index(0), end_index(-1),
        stride(1), n_files(0), n_indices_per_file(1)
    {}

    ~file_mapper()
    {
#if defined(TECA_HAS_MPI)
/*
        for (long i =0; i < n_files; ++i)
            MPI_Comm_free(&this->file_comms[i]);
*/
#endif
    }


    std::vector<teca_metadata> requests;
    std::string index_initializer_key;
    std::string index_request_key;

    // user provided overrides
    long start_index;
    long end_index;
    long stride;

    // indices to request by rank
    long n_indices;
    std::vector<long> block_size;
    std::vector<long> block_start;

    // output files
    long n_files;
    long n_indices_per_file;
    std::vector<std::set<int>> file_ranks;

/*
    std::vector<MPI_Comm> file_comms;
    std::vector<int> file_handles;
    // 
    int n_ranks;
*/

int to_stream(std::ostream &os, MPI_Comm comm)
{
    int rank = 0;
    int n_ranks = 1;
#if defined(TECA_HAS_MPI)
    int is_init = 0;
    MPI_Initialized(&is_init);
    if (is_init)
    {
        MPI_Comm_rank(comm, &rank);
        MPI_Comm_size(comm, &n_ranks);
    }
#endif
    if (rank == 0)
    {
        os << "start_index = " << this->start_index << std::endl
            << "end_index = " << this->end_index << std::endl
            << "n_indices = " << this->n_indices << std::endl
            << "n_indices_per_file = " << this->n_indices_per_file << std::endl
            << "n_files = " << this->n_files << std::endl
            << "n_ranks = " << n_ranks << std::endl
            << "rank\tfirst_index\tlast_index" << std::endl;

        for (int i = 0; i < n_ranks; ++i)
            os << i << "\t" << block_start[i] << "\t"
                << block_start[i] + block_size[i] - 1 << std::endl;

        os << "file\tranks" << std::endl;
        for (int i = 0; i < this->n_files; ++i)
        {
            os << i << "\t";
            std::set<int> &f_ranks = this->file_ranks[i];
            std::set<int>::iterator it = f_ranks.begin();
            std::set<int>::iterator end = f_ranks.end();
            for (; it != end; ++it)
            {
                os << *it << ", ";
            }
            os << std::endl;
        }
    }

    return 0;
}

// --------------------------------------------------------------------------
int get_upstream_requests(MPI_Comm comm, teca_metadata base_req,
    std::vector<teca_metadata> &up_reqs)
{
    int rank = 0;
    int n_ranks = 1;
#if defined(TECA_HAS_MPI)
    int is_init = 0;
    MPI_Initialized(&is_init);
    if (is_init)
    {
        MPI_Comm_rank(comm, &rank);
        MPI_Comm_size(comm, &n_ranks);
    }
#endif
    // apply the base request to local indices.
    long n_req = this->block_size[rank];
    long first = this->block_start[rank];
    up_reqs.reserve(n_req);
    for (long i = 0; i < n_req; ++i)
    {
        long index = i + first;
        up_reqs.push_back(base_req);
        up_reqs.back().set(this->index_request_key, index);
    }
    return 0;
}

// --------------------------------------------------------------------------
int alloc_communicators(MPI_Comm comm, std::vector<MPI_Comm> &file_comms)
{
    // create communicator for each file
    file_comms.resize(this->n_files, comm);
#if defined(TECA_HAS_MPI)
    int is_init = 0;
    MPI_Initialized(&is_init);
    if (is_init)
    {
        int rank = 0;
        int n_ranks = 1;
        MPI_Comm_rank(comm, &rank);
        MPI_Comm_size(comm, &n_ranks);
        if (n_ranks > 1)
        {
            // parallel run. partition ranks to files and make communicators
            // that encode the partitioning.
            for (long i = 0; i < this->n_files; ++i)
            {
                std::set<int> &file_ranks_i = this->file_ranks[i];
                int color = MPI_UNDEFINED;
                if (file_ranks_i.find(rank) != file_ranks_i.end())
                    color = 0;

                MPI_Comm file_comm = MPI_COMM_NULL;
                MPI_Comm_split(comm, color, rank, &file_comm);
                file_comms[i] = file_comm;
            }
        }
        else
        {
            // serial run. use the only communicator
            for (long i = 0; i < this->n_files; ++i)
            {
                MPI_Comm file_comm = MPI_COMM_NULL;
                MPI_Comm_dup(comm, &file_comm);
                file_comms[i] = file_comm;
            }
        }
    }
    else
    {
       // mpi is not in use
       for (long i = 0; i < this->n_files; ++i)
           file_comms[i] = comm;
    }
#endif
    return 0;
}

// --------------------------------------------------------------------------
int free_communicators(MPI_Comm comm, std::vector<MPI_Comm> &file_comms)
{
#if defined(TECA_HAS_MPI)
    int is_init = 0;
    MPI_Initialized(&is_init);
    if (is_init)
    {
        for (long i = 0; i < this->n_files; ++i)
        {
            MPI_Comm comm_i = file_comms[i];
            if (comm_i != MPI_COMM_NULL)
            {
                MPI_Comm_free(&file_comms[i]);
                file_comms[i] = MPI_COMM_NULL;
            }
        }
    }
#endif
    return 0;
}


// --------------------------------------------------------------------------
int initialize(MPI_Comm comm, const teca_metadata &md)
{
#if !defined(TECA_HAS_MPI)
    (void)comm;
#endif
    this->requests.clear();

    // locate the keys that enable us to know how many
    // requests we need to make and what key to use
    if (md.get("index_initializer_key", this->index_initializer_key))
    {
        TECA_ERROR("No index initializer key has been specified")
        return -1;
    }

    if (md.get("index_request_key", this->index_request_key))
    {
        TECA_ERROR("No index request key has been specified")
        return -1;
    }

    // locate available indices
    this->n_indices = 0;
    if (md.get(this->index_initializer_key, n_indices))
    {
        TECA_ERROR("metadata is missing the initializer key \""
            << this->index_initializer_key << "\"")
        return -1;
    }

    // apply restriction
    long last
        = this->end_index >= 0 ? this->end_index : n_indices - 1;

    long first
        = ((this->start_index >= 0) && (this->start_index <= last))
            ? this->start_index : 0;

    this->n_indices = last - first + 1;

    // partition indices across MPI ranks. each rank
    // will end up with a unique block of indices
    // to process.
    int rank = 0;
    int n_ranks = 1;
#if defined(TECA_HAS_MPI)
    int is_init = 0;
    MPI_Initialized(&is_init);
    if (is_init)
    {
        MPI_Comm_rank(comm, &rank);
        MPI_Comm_size(comm, &n_ranks);
    }
#endif

    // map indices to ranks
    long n_big_blocks = this->n_indices%n_ranks;
    this->block_size.resize(n_ranks);
    this->block_start.resize(n_ranks);
    for (int i = 0; i < n_ranks; ++i)
    {
        this->block_size[i] = 1;
        this->block_start[i] = 0;
        if (i < n_big_blocks)
        {
            this->block_size[i] = this->n_indices/n_ranks + 1;
            this->block_start[i] = first + this->block_size[i]*i;
        }
        else
        {
            this->block_size[i] = this->n_indices/n_ranks;
            this->block_start[i] = first + this->block_size[i]*i + n_big_blocks;
        }
    }

    // get the number of files to write
    this->n_files = this->n_indices / this->n_indices_per_file +
        (this->n_indices % this->n_indices_per_file ? 1 : 0);

    // map file id to ranks
    this->file_ranks.resize(this->n_files);
    int last_file_rank = 0;
    std::vector<int> file_ranks_i;
    file_ranks_i.reserve(n_ranks);
    for (long i = 0; i < this->n_files; ++i)
    {
        long file_index_0 = i*this->n_indices_per_file;
        long file_index_1 = file_index_0 + this->n_indices_per_file - 1;

        file_ranks_i.clear();

        for (int j = last_file_rank; j < n_ranks; ++j)
        {
            long block_index_0 = first + this->block_start[j];
            long block_index_1 = block_index_0 + this->block_size[j] - 1;

            // check if this rank is writing to this file
            long bf_int_0 = file_index_0 > block_index_0 ?
                 file_index_0 : block_index_0;

            long bf_int_1 = file_index_1 < block_index_1 ?
                file_index_1 : block_index_1;
            if (bf_int_0 <= bf_int_1)
            {
                // yes add it to the list
                file_ranks_i.push_back(j);
            }
        }

        last_file_rank = file_ranks_i.size() ? file_ranks_i[0] : 0;

        // store for a later look up
        this->file_ranks[i].insert(file_ranks_i.begin(), file_ranks_i.end());
    }


    return 0;
}
};




int main(int argc, char **argv)
{
    teca_mpi_manager mpi_man(argc, argv);
    int rank = mpi_man.get_comm_rank();

    teca_system_interface::set_stack_trace_on_error();
    teca_system_interface::set_stack_trace_on_mpi_error();


    if (argc != 3)
    {
        std::cerr << "usage: a.out "
            "[num indices] [num steps per file]" << std::endl;
        return -1;
    }

    long n_steps = atoi(argv[1]);
    long n_steps_per_file = atoi(argv[2]);

    teca_metadata md;
    md.set("index_initializer_key", std::string("n_steps"));
    md.set("index_request_key", std::string("step"));
    md.set("n_steps", n_steps);

    file_mapper fm;
    fm.n_indices_per_file = n_steps_per_file;
    fm.initialize(MPI_COMM_WORLD, md);
    fm.to_stream(std::cerr, MPI_COMM_WORLD);

    std::vector<MPI_Comm> comms;
    fm.alloc_communicators(MPI_COMM_WORLD, comms);
    fm.free_communicators(MPI_COMM_WORLD, comms);

    return 0;
}





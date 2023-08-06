#ifndef teca_cf_file_layout_h
#define teca_cf_file_layout_h

#include "teca_variant_array.h"
#include "teca_metadata.h"
#include "teca_array_collection.h"
#include "teca_mpi.h"

#include <vector>
#include <string>


// defines the API for writing data independant dof how it
// is layed out on disk
class teca_cf_file_layout
{
public:
    virtual ~teca_cf_file_layout() {}

    // creates the NetCDF file.
    virtual int create(MPI_Comm comm, unsigned long file_id,
        unsigned long first_index, unsigned long n_indices,
        const std::string &file_name, const std::string &date_format,
        const teca_metadata &md_in, int mode_flags,
        int use_unlimited_dim) = 0;

    // defines the NetCDF file file_layout.
    virtual int define(const const_p_teca_variant_array &x,
        const const_p_teca_variant_array &y, const const_p_teca_variant_array &z,
        const std::string &x_variable, const std::string &y_variable,
        const std::string &z_variable,
        const std::vector<const_p_teca_array_collection> &point_arrays,
        const std::vector<const_p_teca_array_collection> &info_arrays,
        int compression_level, const teca_metadata &md_in) = 0;

    // writes the colllection of arrays to the NetCDF file
    // in the correct spot.
    virtual int write(const std::vector<long> &request_ids,
        const std::vector<const_p_teca_array_collection> &point_arrays,
        const std::vector<const_p_teca_array_collection> &info_arrays) = 0;

    // close the file
    virtual int close() = 0;

    // return true if the file is open and can be written to
    virtual bool opened() = 0;

    // return true if the file has been defined in the NetCDF sense.
    virtual bool defined() = 0;
};


#endif

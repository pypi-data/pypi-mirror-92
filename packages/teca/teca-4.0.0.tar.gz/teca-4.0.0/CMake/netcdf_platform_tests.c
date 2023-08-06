#ifdef NETCDF_MPI_TEST
#include <mpi.h>
#include <netcdf.h>
#include <netcdf_par.h>
int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);

    int  fh = 0;
    int ierr = nc_create_par("test_create_par.nc", NC_NETCDF4,
        MPI_COMM_WORLD, MPI_INFO_NULL, &fh);

    if (ierr != NC_NOERR)
    {
        return 1;
    }

    nc_close(fh);

    MPI_Finalize();

    return 0;
}
#endif

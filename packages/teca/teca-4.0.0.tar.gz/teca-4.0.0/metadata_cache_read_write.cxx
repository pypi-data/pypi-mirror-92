


// locate files
/*
        std::vector<std::string> files;
        std::string path;

        if (!this->file_names.empty())
        {
            // use file name
            size_t n_file_names = this->file_names.size();
            for (size_t i = 0; i < n_file_names; ++i)
            {
                std::string file_name = this->file_names[i];
                files.push_back(teca_file_util::filename(file_name));
            }
            path = (n_file_names ?
                teca_file_util::path(this->file_names[0]) : std::string());
        }
        else
        {
            // use regex
            std::string regex = teca_file_util::filename(this->files_regex);
            path = teca_file_util::path(this->files_regex);

            if (teca_file_util::locate_files(path, regex, files))
            {
                TECA_ERROR(
                    << "Failed to locate any files" << endl
                    << this->files_regex << endl
                    << path << endl
                    << regex)
                return teca_metadata();
            }
        }

*/



// read cache file
/*
#if defined(TECA_HAS_OPENSSL)
        // look for a metadata cache. we are caching it on disk as for large
        // datasets on Lustre, scanning the time dimension is costly because of
        // NetCDF CF convention that time is unlimitted and thus not layed out
        // contiguously in the files.
        std::string metadata_cache_key;

        std::string metadata_cache_path[4] =
            {(getenv("HOME") ? : "."), ".", path, metadata_cache_dir};

        int n_metadata_cache_paths = metadata_cache_dir.empty() ? 2 : 3;

        if (this->cache_metadata)
        {
            // the key should include runtime attributes that change the metadata
            teca_binary_stream bs;

            bs.pack(path);
            bs.pack(files);

            bs.pack(this->files_regex);
            bs.pack(this->file_names);
            bs.pack(this->x_axis_variable);
            bs.pack(this->y_axis_variable);
            bs.pack(this->z_axis_variable);
            bs.pack(this->t_axis_variable);
            bs.pack(this->t_units);
            bs.pack(this->t_calendar);
            bs.pack(this->t_values);
            bs.pack(this->filename_time_template);
            bs.pack(this->periodic_in_x);
            bs.pack(this->periodic_in_y);
            bs.pack(this->periodic_in_z);

            metadata_cache_key =
                this->internals->create_metadata_cache_key(bs);

            for (int i = n_metadata_cache_paths; i >= 0; --i)
            {
                std::string metadata_cache_file =
                    metadata_cache_path[i] + PATH_SEP + "." + metadata_cache_key + ".tmd";

                if (teca_file_util::file_exists(metadata_cache_file.c_str()))
                {
                    // read the cache
                    if (teca_file_util::read_stream(metadata_cache_file.c_str(),
                        "teca_cf_reader::metadata_cache_file", stream))
                    {
                        TECA_WARNING("Failed to read metadata cache \""
                            << metadata_cache_file << "\"")
                    }
                    else
                    {
                        TECA_STATUS("Found metadata cache \""
                            << metadata_cache_file << "\"")
                        // recover metadata
                        this->internals->metadata.from_stream(stream);
                        // stop
                        break;
                    }
                }
            }
        }
#endif
*/

// write cache file
/*
#if defined(TECA_HAS_OPENSSL)
            if (this->cache_metadata)
            {
                // cache metadata on disk
                bool cached_metadata = false;
                for (int i = n_metadata_cache_paths; i >= 0; --i)
                {
                    std::string metadata_cache_file =
                        metadata_cache_path[i] + PATH_SEP + "." + metadata_cache_key + ".tmd";

                    if (!teca_file_util::write_stream(metadata_cache_file.c_str(),
                        S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP|S_IROTH,
                        "teca_cf_reader::metadata_cache_file", stream, false))
                    {
                        cached_metadata = true;
                        TECA_STATUS("Wrote metadata cache \""
                            << metadata_cache_file << "\"")
                        break;
                    }
                }
                if (!cached_metadata)
                {
                    TECA_ERROR("failed to create a metadata cache")
                }
            }
#endif
*/

// threaded read
/*
            // collect time steps from this and the rest of the files.
            // there are a couple of  performance issues on Lustre.
            // 1) opening a file is slow, there's latency due to contentions
            // 2) reading the time axis is very slow as it's not stored
            //    contiguously by convention. ie. time is an "unlimted"
            //    NetCDF dimension.
            // when procesing large numbers of files these issues kill
            // serial performance. hence we are reading time dimension
            // in parallel.
            using teca_netcdf_util::read_variable_and_attributes;

            read_variable_and_attributes::queue_t
                thread_pool(MPI_COMM_SELF, this->thread_pool_size, true, false);

                // assign the reads to threads
                size_t n_files = files.size();
                for (size_t i = 0; i < n_files; ++i)
                {
                    read_variable_and_attributes
                         reader(path, files[i], i, t_axis_variable);

                    read_variable_and_attributes::task_t task(reader);

                    thread_pool.push_task(task);
                }

                // wait for the results
                std::vector<read_variable_and_attributes::data_t> tmp;
                tmp.reserve(n_files);
                thread_pool.wait_all(tmp);

                // unpack the results. map is used to ensure the correct
                // file to time association.
                std::map<unsigned long, read_variable_and_attributes::data_elem_t>
                    time_arrays(tmp.begin(), tmp.end());
*/


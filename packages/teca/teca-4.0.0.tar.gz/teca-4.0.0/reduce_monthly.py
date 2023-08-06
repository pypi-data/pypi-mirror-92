from teca import *

class time_point:
    """
    A structure holding a floating point time value and its
    corresponding year, month day, hour minute and second
    """
    def __init__(self, t, units, calendar):
        self.t = t
        self.units = units
        self.calendar = calendar

        self.year, self.month, self.day, \
            self.hour, self.minutes, self.seconds = \
                coordinate_util.date(t, self.units, self.calendar)

    def __str__(self):
        return '%g (%s, %s) --> %04d-%02d-%02d %02d:%02d:%02g'%(
            self.t, self.units, self.calendar, self.year, self.month, self.day,
                 self.hour, self.minutes, self.seconds)


class c_struct:
    """
    A c like data structure
    """
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def __str__(self):
        strg = ''
        for k,v in self.__dict__.items():
            strg += k + '=' + str(v) + ', '
        return strg


class month_iterator:
    """
    An iterator over all months between 2 time_point's. A pair
    of time steps bracketing the current month are returned at
    each iteration.
    """

    def __init__(self, t, units, calendar):
        """
        t - an array of floating point time values
        units - string units of the time values
        calendar - string name of the calendar system
        """
        # time values
        self.t = t
        self.units = units
        self.calendar = calendar
        # time point's to iterate between
        self.t0 = time_point(t[0], units, calendar)
        self.t1 = time_point(t[-1], units, calendar)
        # current time state
        self.year = self.t0.year
        self.month = self.t0.month

    def last_day_of_month(self):
        """
        Get's the number of days in the month, with logic for
        leap years
        """

        days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if (self.month == 2) and \
            (self.year % 100  == 0) and (self.year % 400 == 0):
            days[2] = 29

        return days[self.month]

    def __iter__(self):
        return self

    def __next__(self):
        """
        return a pair of time steps bracketing the current month.
        both returned time steps belong to the current month.
        """
        # check for more months to process
        if (self.year > self.t1.year) or \
            (self.year == self.t1.year) and (self.month > self.t1.month):
            raise StopIteration

        # find the time step of the first day
        year = self.year
        month = self.month

        t0 = '%04d-%02d-01 00:00:00'%(self.year, self.month)
        i0 = coordinate_util.time_step_of(self.t, True, self.calendar, self.units, t0)

        # find the time step of the last day
        n_days = self.last_day_of_month()
        t1 = '%04d-%02d-%02d 11:59:59'%(self.year, self.month, n_days)
        i1 = coordinate_util.time_step_of(self.t, True, self.calendar, self.units, t1)

        # move to next month
        self.month += 1

        # move to next year
        if self.month == 13:
            self.month = 1
            self.year += 1

        return c_struct(time=self.t[i0], year=year, month=month,
                        n_days=n_days, start_index=i0, end_index=i1)


class monthly_average(teca_python_algorithm):
    def __init__(self):
        try:
            self.rank = MPI.COMM_WORLD.Get_rank()
        except:
            self.rank = 0
        self.indices = []
        self.metadata = None
        self.arrays = []

    def get_stream_size(self):
        # this enables streaming mode
        return 2

    def get_number_of_threads(self):
        return 2

    def set_arrays(self, arrays):
        self.arrays = arrays

    def report(self, port, md_in):
        sys.stderr.write('[%d] monthly_average::report\n'%(self.rank))

        md_out = md_in[0]

        # get the time axis
        atts = md_out['attributes']
        coords = md_out['coordinates']

        t = coords['t']
        t_var = coords['t_variable']

        t_atts = atts[t_var]
        cal = t_atts['calendar']
        t_units = t_atts['units']

        # convert to a monthly delta t
        self.indices = [ii for ii in month_iterator(t, t_units, cal)]

        # update the control keys
        initializer_key = md_out['index_initializer_key']
        md_out[initializer_key] = len(self.indices)

        # update the metadata
        out_atts = teca_metadata()
        out_vars = []

        for array in self.arrays:
            # name of the output array
            out_vars.append(array)

            # pass the attributes
            in_atts = atts[array]
            in_atts['description'] =  'monthly average of %s'%(array)

            out_atts[array] = in_atts

        # update time axis
        q = 0
        t_out = np.empty(len(self.indices), dtype=np.float64)
        for ii in self.indices:
            t_out[q] = ii.time
            q += 1
        coords['t'] = t_out
        md_out['coordinates'] = coords

        out_atts[t_var] = t_atts

        md_out['variables'] = out_vars
        md_out["attributes"] = out_atts

        return md_out

    def request(self, port, md_in, req_in):
        sys.stderr.write('[%d] monthly_average::request\n'%(self.rank))

        md = md_in[0]
        request_key = md['index_request_key']

        # generate one request for each time step in the month
        req_id = req_in[request_key]
        ii = self.indices[req_id]
        up_reqs = []
        i = ii.start_index
        while i <= ii.end_index:
            req = teca_metadata(req_in)
            req[request_key] = i
            up_reqs.append(req)
            i += 1

        return up_reqs

    def execute(self, port, data_in, req_in, streaming):
        sys.stderr.write('[%d] monthly_average::execute %d %d\n'%(self.rank, len(data_in), streaming))

        # copy the first mesh
        mesh_in = as_teca_cartesian_mesh(data_in.pop())
        mesh_out = teca_cartesian_mesh.New()
        mesh_out.copy(mesh_in)
        arrays_out = mesh_out.get_point_arrays()

        # accumulate incoming values
        while len(data_in):
            mesh_in = as_teca_cartesian_mesh(data_in.pop())
            arrays_in = mesh_in.get_point_arrays()
            for array in self.arrays:
                array_in = arrays_in[array]
                array_out = arrays_out[array]
                array_out += array_in
                arrays_out[array] = array_out

        # when all the data is processed
        if not streaming:
            request_key = req_in['index_request_key']
            req_id = req_in[request_key]
            ii = self.indices[req_id]
            for array in self.arrays:
                array_out = arrays_out[array]
                array_out /= ii.n_days
                arrays_out[array] = array_out
            # fix time
            mesh_out.set_time_step(req_id)
            mesh_out.set_time(ii.time)

        return mesh_out


files = sys.argv[1]
arrays = sys.argv[2]

cfr = teca_cf_reader.New()
cfr.set_files_regex(files)

mav = monthly_average.New()
mav.set_input_connection(cfr.get_output_port())
mav.set_arrays([arrays])

cfw = teca_cf_writer.New()
cfw.set_input_connection(mav.get_output_port())
cfw.set_thread_pool_size(1)
cfw.set_file_name('monthly_avg_%t%.nc')
cfw.set_point_arrays([arrays])
cfw.update()

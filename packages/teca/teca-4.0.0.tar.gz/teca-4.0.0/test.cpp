#include <iostream>
#include <memory>
using namespace std;


template<int nc_enum> class cpp_tt {};

#define DECLARE_CPP_TT(_nc_enum, _cpp_t)  \
template <> class cpp_tt<_nc_enum>       \
{                                       \
public:                                 \
    using type = _cpp_t;               \
};
DECLARE_CPP_TT(1, int)
DECLARE_CPP_TT(2, double)




struct package
{
    const char *name;
    int value;
};


void print_package(const package &p)
{
    std::cerr << p.name << "=" << p.value << std::endl;
}


struct A
{
    operator bool ()
    {
        cerr << "conversion to bool!" << endl;
        return true;
    }
};



int main(int, char **)
{
    shared_ptr<A> p1(new A);
    shared_ptr<A> p2;

    cerr << "if(p1) -> ";
    if (p1)
        cerr << "true";
    else
        cerr << "false";
    cerr << endl;

    cerr << "if(*p1)";
    if (*p1)
        cerr << "true";
    else
        cerr << "false";
    cerr << endl;



    print_package({"burl",10});

    cpp_tt<1>::type a = 1.11;
    cpp_tt<2>::type b = 2.65;

    std::cerr << "a=" << a << std::endl
        << "b=" << b << std::endl;



    return 0;
}


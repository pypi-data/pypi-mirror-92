#include <iostream>
#include <limits>
#include <iomanip>
#include <cmath>

template <typename T>
std::ostream &max_prec(std::ostream &os, const T &num)
{
    os << std::setprecision(std::numeric_limits<T>::digits10 + 1) << num;
    return os;
}

template <typename n_t>
struct equal_tt {};

template <>
struct equal_tt<float>
{
    static float relTol() { return 10.0f*std::numeric_limits<float>::epsilon(); }
    static float absTol() { return std::numeric_limits<float>::epsilon(); }
};

template <>
struct equal_tt<double>
{
    static double relTol() { return 10.0*std::numeric_limits<double>::epsilon(); }
    static double absTol() { return std::numeric_limits<float>::epsilon(); }
};

template <>
struct equal_tt<long double>
{
    static long double relTol() { return std::numeric_limits<double>::epsilon(); }
    static long double absTol() { return std::numeric_limits<double>::epsilon(); }
};




template <typename T>
bool equal(T a, T b, T relTol = equal_tt<T>::relTol(), T absTol = equal_tt<T>::absTol())
{
    // for numbers close to zero
    T diff = std::abs(a - b);
    std::cerr << "diff="; max_prec(std::cerr, diff) << std::endl;
    std::cerr << "absTol="; max_prec(std::cerr, absTol) << std::endl;
    if (diff <= absTol)
        return true;
    // realtive difference
    a = std::abs(a);
    b = std::abs(b);
    b = (b > a) ? b : a;
    std::cerr << "b="; max_prec(std::cerr, b) << std::endl;
    b *= relTol;
    std::cerr << "relTol="; max_prec(std::cerr, relTol) << std::endl;
    std::cerr << "b*relTol="; max_prec(std::cerr, b) << std::endl;
    if (diff <= b)
        return true;
    return false;
}

int main(int, char**)
{
    using fp_t = double;
    fp_t a = 1.2345e20;
    fp_t aa = (((a + fp_t(7)*a)  * fp_t(103)) / fp_t(103)) - (fp_t(7) * a);

    fp_t b = sin(fp_t(M_PIl));
    fp_t bb = 0.0f;

    std::cerr << "fp " << sizeof(fp_t) << " eps="; max_prec(std::cerr, std::numeric_limits<fp_t>::epsilon()) << std::endl << std::endl;

    std::cerr << "a="; max_prec(std::cerr, a) << " aa="; max_prec(std::cerr, aa) << std::endl;
    std::cerr << "a == aa ? " << equal(a,aa) << std::endl << std::endl;

    std::cerr << "b="; max_prec(std::cerr, b) << " bb="; max_prec(std::cerr, bb) << std::endl;
    std::cerr << "b == bb ? " << equal(b,bb) << std::endl;

    return 0;
}



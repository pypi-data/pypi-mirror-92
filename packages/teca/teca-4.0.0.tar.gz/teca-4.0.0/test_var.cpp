
#include "teca_variant_array.h"

#include <variant>
#include <cstring>


using fill_value_t =
    std::variant<char, unsigned char, short, unsigned short,
         int, unsigned int, long, unsigned long, long long,
         unsigned long long, float, double>;



int main(int argc, char** argv)
{
    int code = atoi(argv[1]);

    fill_value_t fill_value(1e20f);

    char tmp();
    fill_value = tmp;
/*
    CODE_DISPATCH(10,
        char v();
        fill_value = v;
        )
*/
    return 0;
}

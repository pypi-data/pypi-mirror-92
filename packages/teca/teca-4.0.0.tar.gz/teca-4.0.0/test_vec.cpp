#include <cstdlib>
#include <cstring>
#include <cmath>
#include <iostream>

template<typename n_t, typename m_t>
void mul_tern(size_t n, n_t *r, n_t *a1, n_t *a2, n_t fv, m_t *m)
{
    for (size_t i = 0; i < n; ++i)
    {
        r[i] = m[i] ? a1[i]*a2[i] : fv;
    }
}

template<typename n_t, typename m_t>
void mul_mask(size_t n, n_t *r, n_t *a1, n_t *a2, n_t fv, m_t *m)
{
    for (size_t i = 0; i < n; ++i)
    {
        r[i] = m[i] * a1[i]*a2[i];
    }
}

using mask_type = int;

int main(int agrc, char **argv)
{
    size_t n = atoi(argv[1]);

    float *a = (float*)malloc(n*sizeof(float));
    float *b = (float*)malloc(n*sizeof(float));
    float *c = (float*)malloc(n*sizeof(float));
    mask_type *m = (mask_type*)malloc(n*sizeof(float));

    for (size_t i = 0; i < n; ++i)
        a[i] = M_PI;

    for (size_t i = 0; i < n; ++i)
        b[i] = 7.0;

    for (size_t i = 0; i < n; ++i)
        m[i] = i % 16 ? 1 : 0;

#define MUL_TERN
#ifdef MUL_TERN
    mul_tern(n, c, a, b, 1e20f, m);
#else
    mul_mask(n, c, a, b, 1e20f, m);
#endif

    for (size_t i = 0; i < n; ++i)
        std::cerr << c[i] << " ";


    return 0;
}




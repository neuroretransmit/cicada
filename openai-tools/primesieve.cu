
#include <gmp.h>

__global__ void primeSieve(mpz_t n, mpz_t prime1, mpz_t prime2)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x; // thread id
    mpz_t prime;
    mpz_init(prime);
    while (mpz_cmp_ui(n, 0) > 0)
    {
        // find next prime
        mpz_nextprime(prime, n);
 
        if (i % 2 == 0) // assign prime to prime1
            mpz_set(prime1, prime);
        else // assign prime to prime2
            mpz_set(prime2, prime);
 
        // update n
        mpz_sub(n, n, prime);
    }
    mpz_clear(prime);
}

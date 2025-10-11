#include <stdio.h>
#include <stdlib.h>

#define CACHE_SIZE 1024
#define BLOCK_SIZE 16
#define MEMORY_SIZE 65536
#define NUM_ACCESSES 1000

typedef struct {
    int valid;
    int tag;
} CacheLine;

int main() {
    int numBlocks = CACHE_SIZE / BLOCK_SIZE;
    CacheLine *cache = (CacheLine *)malloc(numBlocks * sizeof(CacheLine));
    for (int i = 0; i < numBlocks; i++) {
        cache[i].valid = 0;
        cache[i].tag = -1;
    }
    int hits = 0, misses = 0;
    for (int i = 0; i < NUM_ACCESSES; i++) {
        int address = rand() % MEMORY_SIZE;
        int blockNumber = address / BLOCK_SIZE;
        int index = blockNumber % numBlocks;
        int tag = blockNumber / numBlocks;
        if (cache[index].valid && cache[index].tag == tag) {
            hits++;
        }
        else {
            misses++;
            cache[index].valid = 1;
            cache[index].tag = tag;
        }
    }
    printf("Cache Size: %d bytes\n", CACHE_SIZE);
    printf("Block Size: %d bytes\n", BLOCK_SIZE);
    printf("Number of Cache Lines: %d\n", numBlocks);
    printf("Total Accesses: %d\n", NUM_ACCESSES);
    printf("Cache Hits: %d\n", hits);
    printf("Cache Misses: %d\n", misses);
    printf("Hit Ratio: %.2f%%\n", (hits * 100.0) / NUM_ACCESSES);
    printf("Miss Ratio: %.2f%%\n", (misses * 100.0) / NUM_ACCESSES);
    free(cache);
    return 0;
}


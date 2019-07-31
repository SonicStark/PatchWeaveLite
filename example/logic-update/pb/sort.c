#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Book {
  char title[50];
  int book_id;
  int rank;
} book;

const char* getfield(char* line, int num)
{
    const char* tok;
    for (tok = strtok(line, ";");
            tok && *tok;
            tok = strtok(NULL, ";\n"))
    {
        if (!--num)
            return tok;
    }
    return NULL;
}

void selectionSort(struct Book list[], int n) {
  int j, i, min, pos;
  struct Book temp;
  i = 0;
  while (i < n) {
    min = list[i].book_id;
    pos = i;
    for (j = i + 1; j < n; j++) {
      if (list[j].book_id < min) {
        min = list[j].book_id;
        pos = j;
      }
    }

    temp = list[i];
    list[i] = list[pos];
    list[pos] = temp;
    i++;
  }

}

int main(int argc, char const *argv[]) {
    if (argc < 2){
      printf("please provide CSV file\n");
      exit(1);
    }
    struct Book books[5];
    FILE* stream = fopen(argv[1], "r");
    char line[1024];
    int i = 0;
    while (fgets(line, 1024, stream))
    {

        strcpy(books[i].title, getfield(strdup(line), 1));
        books[i].book_id = atoi(getfield(strdup(line), 2));
        books[i++].rank = atoi(getfield(strdup(line), 3));
    
    }

  selectionSort(books, 5);

  for (int i = 0; i < 5; i++)
    printf("%s\n", books[i].title);

  return 0;
}

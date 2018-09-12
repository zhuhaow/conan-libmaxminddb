#include <maxminddb.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
  MMDB_s *mmdb = (MMDB_s *)calloc(1, sizeof(MMDB_s));

  if (NULL == mmdb) {
    exit(1);
  }

  int status = MMDB_open("file_does_not_exist", MMDB_MODE_MMAP, mmdb);

  if (status != MMDB_FILE_OPEN_ERROR) {
    exit(1);
  }

  return 0;
}

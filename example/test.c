#include <api.h>
#include <stdio.h>

int main() {
   init_context();
   printf("result %s\n", eval_smt2("(check-sat)"));
   return 0;
}



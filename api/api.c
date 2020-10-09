#include <z3.h>

static Z3_config config;
static Z3_context context;

void init_context() {
   config = Z3_mk_config();
   context = Z3_mk_context(config);
}

void destroy_context() {
   Z3_del_context(context);
   Z3_del_config(config);
   context = NULL;
   config = NULL;
}

const char* eval_smt2(char* input) {
   printf("Input %s\n", input);
   return Z3_eval_smtlib2_string(context, input);
}

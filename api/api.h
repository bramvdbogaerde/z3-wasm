#ifndef Z3_INTERFACE 
#define Z3_INTERFACE

void init_context();
const char* eval_smt2(char* input);
void destroy_context();
#endif

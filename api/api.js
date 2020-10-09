function allocateString(code) {
   return allocate(intArrayFromString(code), ALLOC_NORMAL);
}

function readString(ptr) {
   return UTF8ToString(ptr)
}

const Z3 = {
   init_context: function () {
      _init_context()
   },

   destroy_context: function () {
      _destroy_context()
   },

   eval_smt2: function (code) {
      const ptr = allocateString(code)
      console.log(ptr)
      return readString(_eval_smt2(ptr))
   },


   solve: function (code) {
      this.init_context()
      const ret = this.eval_smt2(code)
      this.destroy_context()
      return ret.trim()
   }
}

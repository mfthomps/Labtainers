void PROG0_init__(PROG0 *data__, BOOL retain) {
  __INIT_VAR(data__->VAR_IN,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->VAR_OUT,__BOOL_LITERAL(FALSE),retain)
}

// Code part
void PROG0_body__(PROG0 *data__) {
  // Initialise TEMP variables

  __SET_VAR(data__->,VAR_OUT,,__GET_VAR(data__->VAR_IN,));

  goto __end;

__end:
  return;
} // PROG0_body__() 






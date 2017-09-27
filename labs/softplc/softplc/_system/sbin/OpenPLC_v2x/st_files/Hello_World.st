PROGRAM My_Program
  VAR
    button AT %IX0.0 : BOOL;
    lamp AT %QX0.0 : BOOL;
  END_VAR
  VAR
    T0 : TOF;
  END_VAR

  T0(IN := button, PT := T#2000ms);
  lamp := T0.Q;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK TaskMain(INTERVAL := T#50ms,PRIORITY := 0);
    PROGRAM Inst0 WITH TaskMain : My_Program;
  END_RESOURCE
END_CONFIGURATION

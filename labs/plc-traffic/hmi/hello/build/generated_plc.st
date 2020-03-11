PROGRAM Hello_World
  VAR
    my_button AT %IX100.0 : BOOL;
    lamp AT %QX100.0 : BOOL;
  END_VAR
  VAR
    TOF0 : TOF;
  END_VAR

  TOF0(IN := my_button, PT := T#2000ms);
  lamp := TOF0.Q;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : Hello_World;
  END_RESOURCE
END_CONFIGURATION

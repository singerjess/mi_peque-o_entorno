set V := {1..235};
set F := {1..127};
set C := {1..21};
param VECINOS[V*V] := read "/test_cases/aux/reps/ady_matrix_0.txt" as "n+";
var x[V*C] binary;
var z[F] binary;
param ESDELCURSO[V*F] := read "/test_cases/aux/reps/courses_matrix_0.txt" as "n+";
maximize cursos_misma_aula: sum <f> in F: z[f];
subto un_solo_color_cada_uno: # constraint 1
    forall <i> in V:
        (sum <c> in C: x[i,c]) == 1;
subto vecinos_de_distinto_color: # constraints 2
    forall <i> in V:
        forall <j> in V:
            forall <c> in C:
                VECINOS[i,j] * (x[i,c]+x[j,c]) <= 1;
subto validez_de_los_zf:
    forall <f> in F:
        forall <i> in V:
            forall <j> in V:
                forall <c> in C:
                    z[f] <= 1 + x[i,c] - ESDELCURSO[j,f] * x[j,c];
                    #if (ESDELCURSO[i,f] == 1 and ESDELCURSO[j,f] == 1) then 
                    #    z[f] <= 1 + x[i,c] - x[j,c] else 0 <= 0 end; 
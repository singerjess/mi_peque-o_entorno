set V := {1..238};
set F := {1..74};
set C := {1..20};
param VECINOS[V*V] := read "/test_cases/aux/reps/ady_matrix_11.txt" as "n+";
var x[V*C] binary;
var z[F] binary;
param ESDELCURSO[F*V] := read "/test_cases/aux/reps/courses_matrix_11.txt" as "n+";
maximize cursos_misma_aula: sum <f> in F: z[f];
subto un_solo_color_cada_uno: # constraint 1
    forall <i> in V:
        (sum <c> in C: x[i,c]) == 1;
subto vecinos_de_distinto_color: # constraints 2
    forall <i> in V:
        forall <j> in V with (VECINOS[i,j] == 1):
            forall <c> in C:
                x[i,c] + x[j,c] <= 1;
subto validez_de_los_zf:
    forall <f> in F:
        forall <i> in V with (ESDELCURSO[f,i] == 1):
            forall <j> in V with (ESDELCURSO[f,j] == 1):
                forall <c> in C:
                    z[f] <= 1 + x[i,c] - x[j,c];
                    #if (ESDELCURSO[i,f] == 1 and ESDELCURSO[j,f] == 1) then 
                    #    z[f] <= 1 + x[i,c] - x[j,c] else 0 <= 0 end; 
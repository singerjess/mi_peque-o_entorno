set CLASES := {1..235};
set CURSOS := {1..127};
param AULAS := 21;
param VECINOS[CLASES*CLASES] := read "/test_cases/aux/reps/ady_matrix_0.txt" as "n+";
var x[CLASES*CLASES] binary;
var z[CURSOS] binary;
param ESDELCURSO[CURSOS*CLASES] := read "/test_cases/aux/reps/courses_matrix_0.txt" as "n+";
param MINIMOSDELCURSO[CURSOS] := read "/test_cases/aux/reps/first_of_each_course_0.txt" as "n+";
param CANTIDADPORCURSO[CURSOS] := read "/test_cases/aux/reps/amount_per_course_0.txt" as "n+";
maximize cursos_misma_aula: sum <f> in CURSOS: z[f];
#maximize cursos_misma_aula: (sum <f> in CURSOS: CANTIDADPORCURSO[f] * x[1,1]);
subto alguien_te_representa:
    forall <i> in CLASES:
        (sum <j> in CLASES: (1-VECINOS[i,j]) * x[j,i]) == 1;
subto no_mas_de_la_cantidad_de_aulas:
    (sum <j> in CLASES:  x[j,j]) <= AULAS;
subto distintos_representantes_si_estan_conectados:
    forall <u> in CLASES:
         forall <v> in CLASES with (VECINOS[u,v] == 0 and u != v):
            forall <w> in CLASES with (VECINOS[v,w] == 1 and VECINOS[u,w] == 0 and w != u): 
                    x[u,v] + x[u,w] <= x[u,u]; 
subto o_todos_o_ninguno:
    forall <f> in CURSOS:
        CANTIDADPORCURSO[f] * z[f] <= (sum <v> in CLASES: (ESDELCURSO[f,v] * x[(MINIMOSDELCURSO[f]+1),v]));

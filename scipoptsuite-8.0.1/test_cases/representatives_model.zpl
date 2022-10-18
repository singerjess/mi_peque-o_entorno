set CLASES := {1..235};
set CURSOS := {1..127};
param AULAS := 21;
param VECINOS[CLASES*CLASES] := read "/test_cases/aux/reps/ady_matrix_0.txt" as "n+";
var x[CLASES*CLASES] binary;
var z[CURSOS] binary;
param ESDELCURSO[CLASES*CURSOS] := read "/test_cases/aux/reps/courses_matrix_0.txt" as "n+";
param MINIMOSDELCURSO[CURSOS] := read "/test_cases/aux/reps/first_of_each_course_0.txt" as "n+";
param CANTIDADPORCURSO[CURSOS] := read "/test_cases/aux/reps/amount_per_course_0.txt" as "n+";
maximize cursos_misma_aula: sum <f> in CURSOS: z[f];
subto cada_uno_tiene_un_representante:
    forall <i> in CLASES:
        (sum <j> in CLASES: VECINOS[i,j] * x[i,j]) == 1;
subto no_mas_de_la_cantidad_de_aulas:
    (sum <j> in CLASES:  x[j,j]) <= AULAS;
subto distintos_representantes_si_estan_conectados:
    forall <u> in CLASES:
         forall <v> in CLASES:
            forall <w> in CLASES:
                if (VECINOS[v,w] == 1) then 
                    x[u,v] + x[u,w] <= x[u,u] else 0 <= 0 end; # si son vecinos, se cumple trivialmente
subto o_todos_o_ninguno:
    forall <f> in CURSOS:
    (sum <v> in CLASES: ESDELCURSO[v,f] * x[(MINIMOSDELCURSO[f]+1),v]) <= CANTIDADPORCURSO[f] * z[f];

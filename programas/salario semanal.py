while True:
    print("bienvenido al programa empresarial para calcular el salario por hora, dia y semana del empleado")
    salario = float(input("por favor ponga el salario mensual que gana: "))
    dias_laborales = int(input("por favor ponga la cantidad de dias que trabaja a la semana: "))
    horas_diarias = int(input("por favor ponga la cantidad de horas que trabaja diariamente: "))
    dias_trabajados_por_mes  = dias_laborales * 4
    tabla =True
    if dias_laborales > 7 or horas_diarias > 16:
        print("esos valores no son posibles")
        tabla = False
    salario_por_dia_trabajado = salario / dias_trabajados_por_mes
    salario_por_semana = salario_por_dia_trabajado * dias_laborales
    salario_por_hora = salario_por_dia_trabajado/horas_diarias
    if tabla:
        print("tiempo  |  salario")
        print("-------------------")
        print(" mes    | $",salario)
        print(" semana | $",salario_por_semana)
        print(" dia    | $",salario_por_dia_trabajado)
        print(" hora   | $",salario_por_hora)


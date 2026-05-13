import streamlit as st

# ==========================================
# CONFIGURACIÓN Y MEMORIA (SESSION STATE)
# ==========================================
st.set_page_config(page_title="Math Pro", page_icon="🔢", layout="centered")

# Inicializar variables en la memoria temporal de la web
if 'memoria' not in st.session_state:
    st.session_state.memoria = None  # Guardaremos el valor siempre en Decimal internamente

# --- FUNCIONES DE LÓGICA MATEMÁTICA ---
def obtener_resultado_decimal_a(destino, valor):
    if destino == "Decimal": return str(valor)
    base = {"Binario": 2, "Octal": 8, "Hexadecimal": 16}[destino]
    if valor == 0: return "0"
    es_negativo = valor < 0
    valor = abs(valor)
    restos = []
    n = valor
    while n > 0:
        restos.append("0123456789ABCDEF"[n % base])
        n //= base
    resultado = ''.join(restos[::-1])
    return f"-{resultado}" if es_negativo else resultado

def dibujar_division_larga(valor, base, cocientes, restos):
    lines = [f"Divisor: {base}", f"Dividendo: {valor}", "", f"{'Paso':<6}{'Cociente':<12}{'Resto'}"]
    for i, (cociente, resto) in enumerate(zip(cocientes, restos), 1):
        lines.append(f"{i:<6}{cociente:<12}{resto}")
    return "\n".join(lines)

def explicar_decimal_a(destino, valor):
    if destino == "Decimal": return f"El valor ya está en Decimal: {valor}"
    base = {"Binario": 2, "Octal": 8, "Hexadecimal": 16}[destino]
    if valor == 0: return f"Decimal 0 en {destino} es 0."
    
    es_negativo = valor < 0
    n = abs(valor)
    
    pasos, restos_list, cocientes = [], [], []
    while n > 0:
        cociente = n // base
        resto = n % base
        resto_str = "0123456789ABCDEF"[resto]
        pasos.append(f"{n} ÷ {base} = {cociente} resto {resto_str}")
        cocientes.append(cociente)
        restos_list.append(resto_str)
        n = cociente
        
    resultado = ''.join(restos_list[::-1])
    if es_negativo: resultado = "-" + resultado
        
    texto_div = dibujar_division_larga(abs(valor), base, cocientes, restos_list)
    explicacion = f"Convertir decimal {abs(valor)} a {destino} usando divisiones sucesivas:\n\n{texto_div}\n\nPasos:\n" + "\n".join(pasos)
    if es_negativo: explicacion += f"\n\nComo el número original era negativo, añadimos el signo al final."
    explicacion += f"\nResultado: {resultado}"
    return explicacion

def explicar_a_decimal(origen, valor, numero_decimal):
    if origen == "Decimal": return f"El valor ya está en Decimal: {valor}"
    base = {"Binario": 2, "Octal": 8, "Hexadecimal": 16}[origen]
    pasos = []
    
    es_negativo = valor.startswith("-")
    valor_normalizado = valor.replace("-", "").upper()
    
    total = 0
    for i, digito in enumerate(reversed(valor_normalizado)):
        valor_digito = int(digito) if digito.isdigit() else 10 + ord(digito) - ord("A")
        posicion = base ** i
        pasos.append(f"{digito} * {base}^{i} = {valor_digito} * {posicion} = {valor_digito * posicion}")
        total += valor_digito * posicion
        
    if es_negativo: total = -total
    explicacion = f"Convertir {origen.lower()} {valor_normalizado} a decimal:\n\n" + "\n".join(pasos)
    if es_negativo: explicacion += "\n\nSe añade el signo negativo al resultado."
    explicacion += f"\nResultado: {total}"
    return explicacion

def explicar_valor_posicional(origen, destino, valor, numero_decimal):
    if destino == "Decimal": return f"Valor posicional de {origen.lower()} {valor}:\n\n" + explicar_a_decimal(origen, valor, numero_decimal)
    resultado = obtener_resultado_decimal_a(destino, numero_decimal).replace("-", "")
    base = {"Binario": 2, "Octal": 8, "Hexadecimal": 16}[destino]
    partes = []
    for i, digito in enumerate(reversed(resultado)):
        valor_digito = int(digito, 16) if digito.isalpha() else int(digito)
        partes.append(f"{digito} * {base}^{i} = {valor_digito} * {base**i} = {valor_digito * (base**i)}")
    return f"Valor posicional de {destino} {resultado}:\n\n" + "\n".join(partes)


# --- FUNCIONES PARA BOTONES DE MEMORIA ---
def guardar_en_memoria(valor):
    st.session_state.memoria = valor

def borrar_memoria():
    st.session_state.memoria = None

def cargar_memoria_n1():
    base = st.session_state.b1
    st.session_state.n1 = obtener_resultado_decimal_a(base, st.session_state.memoria)

def cargar_memoria_n2():
    base = st.session_state.b2
    st.session_state.n2 = obtener_resultado_decimal_a(base, st.session_state.memoria)


# ==========================================
# BARRA LATERAL (SIDEBAR) - PANEL DE MEMORIA
# ==========================================
with st.sidebar:
    st.header("💾 Panel de Memoria")
    if st.session_state.memoria is not None:
        val_mem = st.session_state.memoria
        st.success(f"**Valor guardado:**")
        st.write(f"🔹 **Dec:** {val_mem}")
        st.write(f"🔹 **Bin:** {obtener_resultado_decimal_a('Binario', val_mem)}")
        st.write(f"🔹 **Oct:** {obtener_resultado_decimal_a('Octal', val_mem)}")
        st.write(f"🔹 **Hex:** {obtener_resultado_decimal_a('Hexadecimal', val_mem)}")
        st.button("🗑️ Vaciar Memoria", on_click=borrar_memoria, use_container_width=True)
    else:
        st.info("La memoria está vacía. Guarda un resultado para usarlo después.")


# ==========================================
# INTERFAZ PRINCIPAL
# ==========================================
st.title("🔢 Math Pro - Sistemas Numéricos")

tab_conversion, tab_operaciones = st.tabs(["🔄 Convertidor", "🧮 Calculadora y Operaciones"])
opciones_bases = ["Decimal", "Binario", "Octal", "Hexadecimal"]
bases_dict = {"Decimal": 10, "Binario": 2, "Octal": 8, "Hexadecimal": 16}

# --- PESTAÑA 1: CONVERTIDOR ---
with tab_conversion:
    st.markdown("Convierte números entre diferentes bases y guárdalos en la memoria.")
    col1, col2 = st.columns(2)
    with col1:
        origen = st.selectbox("Sistema de Origen:", opciones_bases, index=0)
    with col2:
        valor_input = st.text_input(f"Ingresa el valor en {origen}:", "", key="input_conv")

    if valor_input:
        try:
            numero_decimal = int(valor_input, bases_dict[origen])
            
            st.subheader("Resultados:")
            res1, res2, res3, res4 = st.columns(4)
            res1.metric("Decimal", str(numero_decimal))
            res2.metric("Binario", obtener_resultado_decimal_a('Binario', numero_decimal))
            res3.metric("Octal", obtener_resultado_decimal_a('Octal', numero_decimal))
            res4.metric("Hexadecimal", obtener_resultado_decimal_a('Hexadecimal', numero_decimal))

            # Botón para guardar en memoria
            st.button("💾 Guardar este valor en Memoria", on_click=guardar_en_memoria, args=(numero_decimal,))

            st.divider()

            st.subheader("👨‍🏫 Explicación Paso a Paso")
            col_dest, col_check = st.columns(2)
            with col_dest:
                destino = st.selectbox("Sistema de Destino para explicar:", opciones_bases, index=1)
            with col_check:
                st.write("") 
                posicional = st.checkbox("¿Mostrar valor posicional?")

            texto_explicacion = ""
            if origen == destino:
                texto_explicacion = f"El valor ya está en {origen}."
            elif origen == "Decimal":
                texto_explicacion = explicar_decimal_a(destino, numero_decimal)
            elif destino == "Decimal":
                texto_explicacion = explicar_a_decimal(origen, valor_input, numero_decimal)
            else:
                t1 = explicar_a_decimal(origen, valor_input, numero_decimal)
                t2 = explicar_decimal_a(destino, numero_decimal)
                texto_explicacion = f"{t1}\n\n{'-'*30}\n\nLuego convertir de Decimal a {destino}:\n\n{t2}"

            if posicional and origen != destino:
                texto_explicacion += f"\n\n{'-'*30}\n\n" + explicar_valor_posicional(origen, destino, valor_input, numero_decimal)

            st.code(texto_explicacion, language="text")

        except ValueError:
            st.error(f"❌ Asegúrate de ingresar un número válido para {origen}.")


# --- PESTAÑA 2: CALCULADORA ---
with tab_operaciones:
    st.markdown("Realiza operaciones y usa la memoria para cargar números rápidamente.")
    
    col_n1, col_op, col_n2 = st.columns([2, 1, 2])
    
    with col_n1:
        base1 = st.selectbox("Base Num 1:", opciones_bases, index=1, key="b1")
        if st.session_state.memoria is not None:
            st.button("📥 Usar Memoria", key="btn_m1", on_click=cargar_memoria_n1, use_container_width=True)
        num1 = st.text_input("Número 1:", "", key="n1")
        
    with col_op:
        st.write("")
        st.write("")
        if st.session_state.memoria is not None: st.write("") # Espaciado extra
        operacion = st.selectbox("Operación:", ["+", "-", "×", "÷"])
        
    with col_n2:
        base2 = st.selectbox("Base Num 2:", opciones_bases, index=1, key="b2")
        if st.session_state.memoria is not None:
            st.button("📥 Usar Memoria", key="btn_m2", on_click=cargar_memoria_n2, use_container_width=True)
        num2 = st.text_input("Número 2:", "", key="n2")
        
    base_res = st.selectbox("Mostrar resultado final en:", opciones_bases, index=0, key="bres")

    if num1 and num2:
        try:
            dec1 = int(num1, bases_dict[base1])
            dec2 = int(num2, bases_dict[base2])
            
            error_div = False
            if operacion == "+": res_dec = dec1 + dec2
            elif operacion == "-": res_dec = dec1 - dec2
            elif operacion == "×": res_dec = dec1 * dec2
            elif operacion == "÷":
                if dec2 == 0:
                    error_div = True
                    st.error("❌ No se puede dividir entre cero.")
                else:
                    res_dec = dec1 // dec2
                    resto_dec = dec1 % dec2
                    
            if not error_div:
                st.success("¡Cálculo Exitoso!")
                res_final_str = obtener_resultado_decimal_a(base_res, res_dec)
                st.metric(f"Resultado en {base_res}", res_final_str)
                
                # Botón para guardar RESULTADO en memoria
                st.button("💾 Guardar RESULTADO en Memoria", on_click=guardar_en_memoria, args=(res_dec,))
                
                if operacion == "÷" and resto_dec != 0:
                    st.info(f"Nota: Es una división entera. Sobra un resto de {resto_dec} (en decimal).")

                st.divider()
                st.subheader("📝 Procedimiento de la Operación")
                
                proc = []
                if base1 != "Decimal":
                    proc.append(f"PASO 1: Convertir el primer número a Decimal:\n" + explicar_a_decimal(base1, num1, dec1) + "\n" + "="*40)
                if base2 != "Decimal":
                    proc.append(f"PASO 2: Convertir el segundo número a Decimal:\n" + explicar_a_decimal(base2, num2, dec2) + "\n" + "="*40)
                    
                proc.append(f"PASO 3: Realizar la operación en Decimal:")
                if operacion == "÷":
                    proc.append(f"{dec1} ÷ {dec2} = {res_dec} (Cociente) y sobra {resto_dec} (Resto)")
                else:
                    proc.append(f"{dec1} {operacion} {dec2} = {res_dec}")
                proc.append("="*40)
                
                if base_res != "Decimal":
                    proc.append(f"PASO 4: Convertir el resultado ({res_dec}) a {base_res}:\n" + explicar_decimal_a(base_res, res_dec))
                else:
                    proc.append(f"El resultado ya está en Decimal: {res_dec}")
                
                st.code("\n\n".join(proc), language="text")
                
        except ValueError:
            st.error("❌ Hay un error. Revisa que los números escritos coincidan con las bases seleccionadas.")
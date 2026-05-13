import streamlit as st

# ==========================================
# CONFIGURACIÓN Y MEMORIA DOBLE (SESSION STATE)
# ==========================================
st.set_page_config(page_title="Math Pro", page_icon="🔢", layout="centered")

if 'm1' not in st.session_state: st.session_state.m1 = None
if 'm2' not in st.session_state: st.session_state.m2 = None

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


# ---------------------------------------------------------
# FUNCIONES VISUALES DE OPERACIONES BINARIAS (HTML Oscuro)
# ---------------------------------------------------------
def suma_binaria_visual(a_dec, b_dec):
    bin_a = bin(abs(a_dec))[2:]
    bin_b = bin(abs(b_dec))[2:]
    max_len = max(len(bin_a), len(bin_b))
    bin_a = bin_a.zfill(max_len)
    bin_b = bin_b.zfill(max_len)
    acarreos = [''] * (max_len + 1)
    resultado = []
    acarreo_actual = 0
    for i in range(max_len - 1, -1, -1):
        bit_a, bit_b = int(bin_a[i]), int(bin_b[i])
        suma = bit_a + bit_b + acarreo_actual
        resultado.append(str(suma % 2))
        acarreo_actual = suma // 2
        if acarreo_actual > 0: acarreos[i] = '1'
    if acarreo_actual: resultado.append(str(acarreo_actual))
    resultado_final = "".join(resultado[::-1])
    
    linea_acarreos = "  " + " ".join([c if c else " " for c in acarreos[:-1]])
    linea_a = "  " + " ".join(bin_a)
    linea_b = "+ " + " ".join(bin_b)
    if len(resultado_final) > max_len:
        linea_acarreos, linea_a, linea_b = "  " + linea_acarreos, "  " + linea_a, "  " + linea_b
        linea_res = "  " + " ".join(resultado_final)
    else:
        linea_res = "  " + " ".join(resultado_final.zfill(max_len))
    separador = "-" * len(linea_b)

    return f"""<div style="font-family: 'Courier New', monospace; font-size: 18px; background-color: #1e1e1e; color: white; padding: 20px; border-radius: 8px; line-height: 1.6; white-space: pre; border: 1px solid #444;">
<span style="color: #ff4b4b; font-weight: bold;">{linea_acarreos}</span>\n{linea_a}\n{linea_b}\n<span style="color: #888;">{separador}</span>\n<span style="color: #4b8bff; font-weight: bold;">{linea_res}</span></div>"""

def resta_binaria_visual_st(a_dec, b_dec):
    nota = ""
    if abs(b_dec) > abs(a_dec): 
        a_dec, b_dec = b_dec, a_dec
        nota = "<span style='color: #ffcc00; font-size: 14px;'>*Nota: El sustraendo era mayor. Se muestra la resta de los valores absolutos.</span>\n\n"
        
    bin_a = list(bin(abs(a_dec))[2:])
    bin_b = list(bin(abs(b_dec))[2:])
    max_len = max(len(bin_a), len(bin_b))
    bin_a = ["0"] * (max_len - len(bin_a)) + bin_a
    bin_b = ["0"] * (max_len - len(bin_b)) + bin_b
    
    A_orig = bin_a.copy()
    B_orig = bin_b.copy()
    modified_A = [int(x) for x in bin_a]
    B = [int(x) for x in bin_b]
    
    borrows_display = [''] * max_len
    resultado = []
    
    for i in range(max_len - 1, -1, -1):
        if modified_A[i] < B[i]:
            j = i - 1
            while j >= 0 and modified_A[j] == 0:
                modified_A[j] = 1
                borrows_display[j] = '1'
                j -= 1
            if j >= 0:
                modified_A[j] -= 1
                borrows_display[j] = '0'
            modified_A[i] += 2
            borrows_display[i] = '10' # Representa el "2" en binario prestado
        resultado.append(str(modified_A[i] - B[i]))
        
    resultado_final = "".join(resultado[::-1])
    
    ancho = 3
    str_prestamos = "  " + "".join([f"<span style='color: #ff4b4b; font-weight: bold;'>{b.rjust(ancho)}</span>" if b else " " * ancho for b in borrows_display])
    str_a_linea = "  " + "".join([c.rjust(ancho) for c in A_orig])
    str_b_linea = "- " + "".join([c.rjust(ancho) for c in B_orig])
    separador = "-" * (len(str_a_linea) + 2)
    str_res = "  " + "".join([c.rjust(ancho) for c in resultado_final])
    
    return f"""<div style="font-family: 'Courier New', monospace; font-size: 18px; background-color: #1e1e1e; color: white; padding: 20px; border-radius: 8px; line-height: 1.6; white-space: pre; border: 1px solid #444;">{nota}{str_prestamos}\n{str_a_linea}\n{str_b_linea}\n<span style="color: #888;">{separador}</span>\n<span style="color: #4b8bff; font-weight: bold;">{str_res}</span></div>"""

def multiplicacion_binaria_visual_st(a_dec, b_dec):
    bin_a = bin(abs(a_dec))[2:]
    bin_b = bin(abs(b_dec))[2:]
    bin_res = bin(abs(a_dec) * abs(b_dec))[2:]
    max_len = len(bin_res) + 4 
    
    linea_a = bin_a.rjust(max_len)
    linea_b = ("x " + bin_b).rjust(max_len)
    separador1 = ("-" * (len(bin_b) + 2)).rjust(max_len)
    
    pps_full = []
    pps_display = []
    for i, bit in enumerate(reversed(bin_b)):
        if bit == '1':
            pp_full = bin_a + ("0" * i)
            pp_disp = bin_a + (" " * i)
        else:
            pp_full = ("0" * len(bin_a)) + ("0" * i)
            pp_disp = ("0" * len(bin_a)) + (" " * i)
        pps_full.append(pp_full.zfill(max_len))
        pps_display.append(pp_disp.rjust(max_len))
        
    acarreos = [' '] * max_len
    carry = 0
    for col in range(max_len - 1, -1, -1):
        col_sum = carry
        for pp in pps_full:
            col_sum += int(pp[col])
        carry = col_sum // 2
        if carry > 0 and col > 0:
            char_carry = str(carry) if carry < 10 else chr(55 + carry)
            acarreos[col - 1] = char_carry
            
    linea_acarreos = "".join(acarreos)
    
    html = f"""<div style="font-family: 'Courier New', monospace; font-size: 18px; background-color: #1e1e1e; color: white; padding: 20px; border-radius: 8px; line-height: 1.6; white-space: pre; border: 1px solid #444;">
{linea_a}
{linea_b}
<span style="color: #888;">{separador1}</span>
<span style="color: #ff4b4b; font-weight: bold;">{linea_acarreos}</span>
"""
    for pp in pps_display:
        html += f"{pp}\n"
        
    separador2 = ("-" * max(len(bin_res), len(bin_a)+2)).rjust(max_len)
    linea_res = bin_res.rjust(max_len)
    html += f"""<span style="color: #888;">{separador2}</span>\n<span style="color: #4b8bff; font-weight: bold;">{linea_res}</span></div>"""
    return html

def division_binaria_visual_st(dividendo_dec, divisor_dec):
    if divisor_dec == 0:
        return "<p style='color: #ff4b4b; font-weight: bold;'>❌ Error: División por cero</p>"
    
    dvd = bin(abs(dividendo_dec))[2:]
    dvs = bin(abs(divisor_dec))[2:]
    cociente = ""
    residuo_actual = ""
    html_steps = ""
    
    for i in range(len(dvd)):
        bit_actual = dvd[i]
        residuo_actual = (residuo_actual + bit_actual).lstrip('0') or '0'
        val_residuo = int(residuo_actual, 2)
        offset_base = len(dvs) + 3
        
        if val_residuo >= abs(divisor_dec):
            cociente += "1"
            spaces_subtrahend = " " * (offset_base + i - len(dvs) + 1)
            html_steps += f"{spaces_subtrahend}-<span style='color: #ccc;'>{dvs}</span>\n"
            separador = "-" * len(dvs)
            html_steps += f"{spaces_subtrahend} <span style='color: #888;'>{separador}</span>\n"
            
            residuo_actual = bin(val_residuo - abs(divisor_dec))[2:]
            spaces_residuo = " " * (offset_base + i - len(residuo_actual) + 1)
            html_steps += f"{spaces_residuo} <span style='color: #ff4b4b; font-weight: bold;'>{residuo_actual}</span>\n"
        else:
            cociente += "0"
            
    if not cociente: cociente = "0"
    offset_base = len(dvs) + 3
    espacios_cociente = " " * offset_base
    
    html = f"""<div style="font-family: 'Courier New', monospace; font-size: 18px; background-color: #1e1e1e; color: white; padding: 20px; border-radius: 8px; line-height: 1.6; white-space: pre; border: 1px solid #444;">
{espacios_cociente}<span style="color: #4b8bff; font-weight: bold;">{cociente.lstrip('0') or '0'}</span>
{espacios_cociente}<span style="color: #888;">{'-' * len(dvd)}</span>
{dvs} | {dvd}
{html_steps}
<span style="color: #888;">--------------------</span>
<b>Residuo Final:</b> <span style="color: #ff4b4b; font-weight: bold;">{residuo_actual or '0'}</span> (Binario)
<b>Cociente:</b>      <span style="color: #4b8bff; font-weight: bold;">{cociente.lstrip('0') or '0'}</span> (Binario)
</div>"""
    return html


# --- FUNCIONES DE CONTROL DE MEMORIA ---
def guardar_m1(valor): st.session_state.m1 = valor
def guardar_m2(valor): st.session_state.m2 = valor
def borrar_m1(): st.session_state.m1 = None
def borrar_m2(): st.session_state.m2 = None
def vaciar_ambas(): st.session_state.m1 = None; st.session_state.m2 = None

def cargar_en_input(target_input, target_base_key, mem_slot):
    base = st.session_state[target_base_key]
    val_decimal = st.session_state[mem_slot]
    st.session_state[target_input] = obtener_resultado_decimal_a(base, val_decimal)


# ==========================================
# BARRA LATERAL (SIDEBAR) - DOBLE MEMORIA
# ==========================================
with st.sidebar:
    st.header("💾 Panel de Memoria")
    st.subheader("Memoria 1 (M1)")
    if st.session_state.m1 is not None:
        v1 = st.session_state.m1
        st.success(f"**Dec:** {v1}  \n**Bin:** {obtener_resultado_decimal_a('Binario', v1)}  \n**Oct:** {obtener_resultado_decimal_a('Octal', v1)}  \n**Hex:** {obtener_resultado_decimal_a('Hexadecimal', v1)}")
        st.button("🗑️ Borrar M1", on_click=borrar_m1, key="b_del_m1")
    else: st.info("M1 está vacía.")

    st.divider()
    st.subheader("Memoria 2 (M2)")
    if st.session_state.m2 is not None:
        v2 = st.session_state.m2
        st.success(f"**Dec:** {v2}  \n**Bin:** {obtener_resultado_decimal_a('Binario', v2)}  \n**Oct:** {obtener_resultado_decimal_a('Octal', v2)}  \n**Hex:** {obtener_resultado_decimal_a('Hexadecimal', v2)}")
        st.button("🗑️ Borrar M2", on_click=borrar_m2, key="b_del_m2")
    else: st.info("M2 está vacía.")

    if st.session_state.m1 is not None or st.session_state.m2 is not None:
        st.divider()
        st.button("🗑️ Vaciar Ambas", on_click=vaciar_ambas, use_container_width=True, type="primary")


# ==========================================
# INTERFAZ PRINCIPAL
# ==========================================
st.title("🔢 Math Pro - Sistemas Numéricos")

tab_conversion, tab_operaciones = st.tabs(["🔄 Convertidor", "🧮 Calculadora y Operaciones"])
opciones_bases = ["Decimal", "Binario", "Octal", "Hexadecimal"]
bases_dict = {"Decimal": 10, "Binario": 2, "Octal": 8, "Hexadecimal": 16}

# --- PESTAÑA 1: CONVERTIDOR ---
with tab_conversion:
    st.markdown("Convierte números y guárdalos en **M1** o **M2**.")
    col1, col2 = st.columns(2)
    with col1: origen = st.selectbox("Sistema de Origen:", opciones_bases, index=0)
    with col2: valor_input = st.text_input(f"Ingresa el valor en {origen}:", "", key="input_conv")

    if valor_input:
        try:
            numero_decimal = int(valor_input, bases_dict[origen])
            st.subheader("Resultados:")
            res1, res2, res3, res4 = st.columns(4)
            res1.metric("Decimal", str(numero_decimal))
            res2.metric("Binario", obtener_resultado_decimal_a('Binario', numero_decimal))
            res3.metric("Octal", obtener_resultado_decimal_a('Octal', numero_decimal))
            res4.metric("Hexadecimal", obtener_resultado_decimal_a('Hexadecimal', numero_decimal))

            st.write("**Guardar este valor en:**")
            g1, g2 = st.columns(2)
            g1.button("💾 Guardar en M1", on_click=guardar_m1, args=(numero_decimal,), use_container_width=True, key="save_conv_m1")
            g2.button("💾 Guardar en M2", on_click=guardar_m2, args=(numero_decimal,), use_container_width=True, key="save_conv_m2")

            st.divider()
            st.subheader("👨‍🏫 Explicación Paso a Paso")
            col_dest, col_check = st.columns(2)
            with col_dest: destino = st.selectbox("Sistema de Destino para explicar:", opciones_bases, index=1)
            with col_check: 
                st.write("") 
                posicional = st.checkbox("¿Mostrar valor posicional?")

            texto_explicacion = ""
            if origen == destino: texto_explicacion = f"El valor ya está en {origen}."
            elif origen == "Decimal": texto_explicacion = explicar_decimal_a(destino, numero_decimal)
            elif destino == "Decimal": texto_explicacion = explicar_a_decimal(origen, valor_input, numero_decimal)
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
    st.markdown("Realiza operaciones usando tus valores guardados en **M1** y **M2**.")
    col_n1, col_op, col_n2 = st.columns([2, 1, 2])
    
    with col_n1:
        base1 = st.selectbox("Base Num 1:", opciones_bases, index=1, key="b1")
        bt1, bt2 = st.columns(2)
        if st.session_state.m1 is not None: bt1.button("📥 Usar M1", key="btn_n1_m1", on_click=cargar_en_input, args=("n1", "b1", "m1"), use_container_width=True)
        if st.session_state.m2 is not None: bt2.button("📥 Usar M2", key="btn_n1_m2", on_click=cargar_en_input, args=("n1", "b1", "m2"), use_container_width=True)
        num1 = st.text_input("Número 1:", "", key="n1")
        
    with col_op:
        st.write("")
        st.write("")
        if st.session_state.m1 is not None or st.session_state.m2 is not None: st.write("") 
        operacion = st.selectbox("Operación:", ["+", "-", "×", "÷"])
        
    with col_n2:
        base2 = st.selectbox("Base Num 2:", opciones_bases, index=1, key="b2")
        bt3, bt4 = st.columns(2)
        if st.session_state.m1 is not None: bt3.button("📥 Usar M1", key="btn_n2_m1", on_click=cargar_en_input, args=("n2", "b2", "m1"), use_container_width=True)
        if st.session_state.m2 is not None: bt4.button("📥 Usar M2", key="btn_n2_m2", on_click=cargar_en_input, args=("n2", "b2", "m2"), use_container_width=True)
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
                
                st.write("**Guardar resultado en:**")
                gr1, gr2 = st.columns(2)
                gr1.button("💾 Guardar en M1", on_click=guardar_m1, args=(res_dec,), use_container_width=True, key="save_res_m1")
                gr2.button("💾 Guardar en M2", on_click=guardar_m2, args=(res_dec,), use_container_width=True, key="save_res_m2")

                st.divider()
                st.subheader("📝 Procedimiento de la Operación")
                
                # --- VISUALIZACIÓN MAGNÍFICA EN BINARIO ---
                st.markdown(f"**🌟 Procedimiento Visual:**")
                if operacion == "+":
                    st.markdown("*Nota: La suma visual se muestra en sistema Binario.*")
                    st.markdown(suma_binaria_visual(dec1, dec2), unsafe_allow_html=True)
                elif operacion == "-":
                    st.markdown("*Nota: La resta visual se muestra en sistema Binario.*")
                    st.markdown(resta_binaria_visual_st(dec1, dec2), unsafe_allow_html=True)
                elif operacion == "×":
                    st.markdown("*Nota: La multiplicación visual se muestra en sistema Binario.*")
                    st.markdown(multiplicacion_binaria_visual_st(dec1, dec2), unsafe_allow_html=True)
                elif operacion == "÷":
                    st.markdown("*Nota: La división visual se muestra en sistema Binario.*")
                    st.markdown(division_binaria_visual_st(dec1, dec2), unsafe_allow_html=True)
                
                st.write("") # Espacio
                
                # --- TEXTO PROCEDIMIENTO NORMAL ---
                proc = []
                if base1 != "Decimal":
                    texto_p1 = f"PASO 1: Convertir el primer número a Decimal:\n{explicar_a_decimal(base1, num1, dec1)}\n{'='*40}"
                    proc.append(texto_p1)
                
                if base2 != "Decimal":
                    texto_p2 = f"PASO 2: Convertir el segundo número a Decimal:\n{explicar_a_decimal(base2, num2, dec2)}\n{'='*40}"
                    proc.append(texto_p2)
                    
                texto_p3 = f"PASO 3: Realizar la operación en Decimal:"
                if operacion == "÷":
                    texto_p3 += f"\n{dec1} ÷ {dec2} = {res_dec} (Cociente) y sobra {resto_dec} (Resto)"
                else:
                    texto_p3 += f"\n{dec1} {operacion} {dec2} = {res_dec}"
                texto_p3 += f"\n{'='*40}"
                proc.append(texto_p3)
                
                if base_res != "Decimal":
                    texto_p4 = f"PASO 4: Convertir el resultado ({res_dec}) a {base_res}:\n{explicar_decimal_a(base_res, res_dec)}"
                    proc.append(texto_p4)
                else:
                    proc.append(f"El resultado ya está en Decimal: {res_dec}")
                
                st.code("\n\n".join(proc), language="text")
                
        except ValueError:
            st.error("❌ Hay un error. Revisa que los números escritos coincidan con las bases seleccionadas.")

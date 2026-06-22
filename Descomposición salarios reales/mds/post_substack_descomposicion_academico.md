# Guía Metodológica: Descomposición del Crecimiento del Salario Real mediante Growth Accounting

El análisis de la evolución del poder adquisitivo de los trabajadores es uno de los campos más complejos de la macroeconomía aplicada. Frecuentemente, el debate público se simplifica en torno a métricas agregadas que ocultan los verdaderos engranajes subyacentes. El objetivo de esta guía es detallar la metodología cuantitativa de contabilidad del crecimiento (*growth accounting*) utilizada para descomponer la evolución del salario real por hora en España durante el ciclo pre-pandemia (1996-2019). 

A través de esta documentación, se exponen las identidades matemáticas a nivel agregado, las técnicas de descomposición sectorial (*within-between*), el empalme de bases de datos de precios incompatibles y la estructura de procesamiento de datos utilizando los consorcios de EUKLEMS e INTANProd. Finalmente, se analiza desde una perspectiva estrictamente contable cómo los shocks del bienio 2020-2021 distorsionan el diagnóstico estructural, justificando la necesidad metodológica de truncar la serie en 2019.

---

## 1. El modelo matemático agregado: La identidad del salario real

El salario real por hora representa el poder de compra de la remuneración media que recibe un asalariado por cada hora de trabajo efectivo. Contablemente, esta variable se puede descomponer de forma exacta como el resultado de tres dimensiones: la distribución primaria de la renta, la eficiencia física del trabajo y los términos de intercambio internos de precios.

### Derivación formal paso a paso

Definamos las variables nominales y reales agregadas de una economía en un periodo $t$:

*   $LAB_t$: Compensación nominal total del factor trabajo. Incluye los salarios brutos de los asalariados, las cotizaciones sociales a la Seguridad Social (tanto las del empleador como las del empleado) y una imputación contable para remunerar el trabajo de los autónomos (para evitar subestimar la renta laboral en economías con alto empleo por cuenta propia).
*   $H_t$: Suma total de las horas de trabajo efectivamente realizadas por ocupados y asalariados.
*   $VA_t$: Valor Añadido Bruto nominal a precios corrientes (VAB nominal).
*   $VA_{Q,t}$: Valor Añadido Bruto real en volumen encadenado (VAB real).
*   $P_{c,t}$: Índice de precios de consumo (IPC), representativo del deflactor de consumo final de los hogares.

A partir de estas variables macroeconómicas primarias, derivamos los siguientes ratios fundamentales:

1.  **Compensación laboral nominal media por hora ($W_t$)**:
    $$W_t = \frac{LAB_t}{H_t}$$

2.  **Participación del factor trabajo en la renta nacional o *Labor Share* ($s_{L,t}$)**:
    $$s_{L,t} = \frac{LAB_t}{VA_t}$$

3.  **Deflactor del Valor Añadido ($P_{VA,t}$)**, que mide la evolución de los precios de producción nacional:
    $$P_{VA,t} = \frac{VA_t}{VA_{Q,t}}$$

Para deducir la identidad del salario real, despejamos la compensación laboral nominal total ($LAB_t$) de la definición de la participación del trabajo ($s_{L,t}$):
$$LAB_t = s_{L,t} \cdot VA_t$$

Sustituyendo esta igualdad en la definición de la compensación laboral nominal por hora ($W_t$):
$$W_t = s_{L,t} \cdot \frac{VA_t}{H_t}$$

Dado que el Valor Añadido nominal es el producto del Valor Añadido real por su deflactor implícito ($VA_t = VA_{Q,t} \cdot P_{VA,t}$), podemos reescribir la expresión:
$$W_t = s_{L,t} \cdot \frac{VA_{Q,t} \cdot P_{VA,t}}{H_t}$$

Reagrupando los términos de producción real y de precios de producción, obtenemos:
$$W_t = s_{L,t} \cdot \left(\frac{VA_{Q,t}}{H_t}\right) \cdot P_{VA,t}$$

El salario nominal por hora es el producto de la participación del trabajo por la productividad laboral real por hora ($VA_{Q,t}/H_t$) y por el deflactor de precios de producción nacional ($P_{VA,t}$). 

Para transformar esta relación en términos de poder adquisitivo, dividimos ambos miembros de la ecuación por el índice de precios al consumo ($P_{c,t}$):
$$\frac{W_t}{P_{c,t}} = s_{L,t} \cdot \left(\frac{VA_{Q,t}}{H_t}\right) \cdot \left(\frac{P_{VA,t}}{P_{c,t}}\right)$$

Esta ecuación representa la **identidad del salario real en niveles**. Demuestra de manera formal que el salario real es igual al producto de:
1.  La participación del trabajo ($s_{L,t}$).
2.  La productividad laboral real ($\frac{VA_{Q,t}}{H_t}$).
3.  La relación de precios relativos ($\frac{P_{VA,t}}{P_{c,t}}$), que contablemente actúa como una **cuña de precios** (*price wedge*).

### Formulación en tasas de crecimiento continuas

Para analizar la evolución temporal y cuantificar las contribuciones de cada factor, aplicamos logaritmos naturales en ambos lados de la ecuación:
$$\ln\left(\frac{W_t}{P_{c,t}}\right) = \ln(s_{L,t}) + \ln\left(\frac{VA_{Q,t}}{H_t}\right) + \ln\left(\frac{P_{VA,t}}{P_{c,t}}\right)$$

Aplicando la propiedad del logaritmo de un cociente al último término:
$$\ln\left(\frac{W_t}{P_{c,t}}\right) = \ln(s_{L,t}) + \ln\left(\frac{VA_{Q,t}}{H_t}\right) + \left[\ln(P_{VA,t}) - \ln(P_{c,t})\right]$$

Si tomamos la primera diferencia temporal ($\Delta$), donde $\Delta X_t = X_t - X_{t-1}$, obtenemos la identidad en tasas de variación continua:
$$\Delta \ln\left(\frac{W_t}{P_{c,t}}\right) = \Delta \ln(s_{L,t}) + \Delta \ln\left(\frac{VA_{Q,t}}{H_t}\right) + \left[\Delta \ln(P_{VA,t}) - \Delta \ln(P_{c,t})\right]$$

Esta formulación aditiva permite que el crecimiento del salario real por hora se distribuya de forma exacta entre tres contribuciones medidas en puntos porcentuales (p.p.):
*   **Contribución de la Participación del Trabajo ($\Delta \ln s_{L,t}$)**: Variaciones en la distribución funcional de la renta. Si la renta salarial crece más despacio que la producción nominal, este término resta al salario real.
*   **Contribución de la Productividad Laboral Real ($\Delta \ln (VA_{Q,t}/H_t)$)**: Variación física del VAB real por hora trabajada.
*   **Contribución de la Cuña de Precios ($\Delta \ln P_{VA,t} - \Delta \ln P_{c,t}$)**: Diferencia entre la inflación de la cesta que produce la economía nacional (deflactor de producción) y la inflación de la cesta que adquiere el trabajador (IPC). Si los precios de consumo crecen más rápido que los precios de producción nacional (por ejemplo, debido al encarecimiento de bienes importados como el petróleo y la energía), la cuña de precios es negativa y el salario real crece por debajo de la productividad física.

---

## 2. Descomposición de la productividad laboral real: Enfoque Growth Accounting sectorial

La variación de la productividad laboral agregada real ($\Delta \ln (VA_{Q,tot,t}/H_{tot,t})$) puede abrirse para identificar qué parte se debe a mejoras en el interior de cada sector (*within-industry*) y qué parte responde a la reasignación de empleo entre sectores (*between-industry*).

A nivel de cada sector económico individual $i$, el marco estándar de contabilidad del crecimiento desglosa el crecimiento de la productividad del trabajo a través de la acumulación de factores productivos por hora y el residuo de eficiencia técnica:
$$\Delta \ln\left(\frac{VA_{Q,i,t}}{H_{i,t}}\right) = \text{comp\_lab}_{i,t} + \text{cap\_tic}_{i,t} + \text{cap\_notic}_{i,t} + \text{cap\_intang}_{i,t} + \text{ptf}_{i,t}$$

Donde:
*   $\text{comp\_lab}_{i,t}$ es la contribución de la composición laboral (capital humano o calidad del trabajo), basada en los cambios de cualificación, educación y experiencia de los ocupados del sector $i$.
*   $\text{cap\_tic}_{i,t}$ es la contribución de la intensificación del capital tecnológico tangible (ordenadores, hardware, software integrado y telecomunicaciones) por hora de trabajo en el sector $i$.
*   $\text{cap\_notic}_{i,t}$ es la contribución de la intensificación de capital físico tradicional tangible (maquinaria, instalaciones, naves industriales, infraestructuras y medios de transporte) por hora de trabajo en el sector $i$.
*   $\text{cap\_intang}_{i,t}$ es la contribución de la intensificación de activos intangibles de conocimiento (I+D capitalizado, patentes, bases de datos, software no integrado, diseño de producto, marca corporativa y capital organizativo de gestión).
*   $\text{ptf}_{i,t}$ es la Productividad Total de los Factores sectorial (Residuo de Solow), que mide la ganancia de eficiencia técnica, organizativa y tecnológica con la que el sector combina sus factores de trabajo y capital.

### Ponderación de Törnqvist para la agregación intrasectorial (*Within*)

Para agregar las contribuciones intrasectoriales al total de la economía nacional, el marco de EUKLEMS utiliza una ponderación basada en las horas trabajadas. El ponderador sectorial para la rama de actividad $i$ en el año $t$, denotado como $\bar{w}_{i,t}$, se define como la media de Törnqvist (el promedio simple de la cuota de horas de trabajo del sector en el año actual y en el anterior):
$$\bar{w}_{i,t} = \frac{1}{2} \left( \frac{H_{i,t}}{H_{tot,t}} + \frac{H_{i,t-1}}{H_{tot,t-1}} \right)$$

Con estos pesos sectoriales, calculamos la contribución de cada factor $k$ agregada dentro de las industrias:
$$\text{within\_factor}_{k,t} = \sum_{i} \bar{w}_{i,t} \cdot \left(\frac{CON_{k,i,t}}{100}\right)$$

Donde $CON_{k,i,t}$ es la contribución expresada en puntos porcentuales del factor $k$ en el sector $i$, tal como figura en los registros de EUKLEMS.

### El residuo de reasignación (*Between*)

Dado que el VAB real y las horas agregadas se consolidan de forma no lineal, la variación de la productividad del trabajo agregada ($\Delta \ln (VA_{Q,tot,t}/H_{tot,t})$) diferirá de la suma de las contribuciones intrasectoriales ponderadas. 

Esta diferencia es el **efecto de reasignación sectorial** (o efecto *Between*), que actúa como el residuo algebraico que cierra la identidad:
$$\text{reasignacion}_t = \Delta \ln\left(\frac{VA_{Q,tot,t}}{H_{tot,t}}\right) - \sum_{k} \text{within\_factor}_{k,t}$$

*   Un efecto de **reasignación positivo** indica que las horas de trabajo se han desplazado de manera neta hacia sectores con niveles de productividad o tasas de crecimiento superiores al promedio nacional (reestructuración eficiente).
*   Un efecto de **reasignación negativo** indica que el empleo se ha concentrado en sectores menos productivos o con menores ritmos de ganancia de eficiencia (terciarización improductiva).

---

## 3. Fuentes de datos, mapeo sectorial y metodología de enlace

El procesamiento del modelo se realiza mediante la integración de tres bases de datos primarias.

### A. Estructura de EUKLEMS e INTANProd (Release 2024 - Luiss LLEE)
Las variables agregadas y las contribuciones sectoriales se extraen de la release 2024 de EUKLEMS-INTANProd, coordinada por el Luiss Lab of European Economics (LLEE) de la Universidad Luiss Guido Carli en Roma. Las variables se organizan de la siguiente manera:
1.  **Valores agregados**: De `ES_national accounts.xlsx` se obtienen las hojas `VA_CP` (VAB corriente), `VA_Q` (VAB real en volumen encadenado) e `H_EMP` (horas totales de ocupados).
2.  **Compensación laboral**: De `ES_growth accounts.xlsx` se obtiene `LAB` (compensación nominal del factor trabajo) de la hoja homónima.
3.  **Contribuciones intrasectoriales**: Se cargan las hojas que contienen las contribuciones anuales ya estimadas por el consorcio de crecimiento:
    *   `LP2ConLC` $\rightarrow$ Composición Laboral ($\text{comp\_lab}$)
    *   `LP2ConTangICT` $\rightarrow$ Capital TIC tangible ($\text{cap\_tic}$)
    *   `LP2ConTangNICT` $\rightarrow$ Capital no-TIC tangible ($\text{cap\_notic}$)
    *   `LP2ConIntang` $\rightarrow$ Capital Intangible ($\text{cap\_intang}$)
    *   `LP2ConTFP` $\rightarrow$ Productividad Total de los Factores ($\text{ptf}$)

### B. Mapeo Sectorial MECE de 33 Ramas
Para evitar duplicidades en la agregación (lo que invalidaría las cuotas de horas $\bar{w}_{i,t}$), el código filtra los datos sectoriales aplicando una partición sectorial de **33 ramas MECE** (Mutuamente Excluyentes y Colectivamente Exhaustivas) basadas en la Clasificación NACE Rev. 2:

*   **Ramas Manufactureras (Subsectores de la industria C)**:
    *   `C10-C12`: Industria de la alimentación, bebidas y tabaco.
    *   `C13-C15`: Textil, confección, cuero y calzado.
    *   `C16-C18`: Madera, papel y artes gráficas.
    *   `C19`: Coquerías y refino de petróleo.
    *   `C20`: Industria química.
    *   `C21`: Fabricación de productos farmacéuticos.
    *   `C22-C23`: Caucho, plásticos y otros productos minerales no metálicos.
    *   `C24-C25`: Metalurgia y fabricación de productos metálicos (excepto maquinaria).
    *   `C26`: Fabricación de productos informáticos, electrónicos y ópticos.
    *   `C27`: Fabricación de material y equipo eléctrico.
    *   `C28`: Fabricación de maquinaria y equipo n.c.o.p.
    *   `C29-C30`: Vehículos de motor, remolques y otro material de transporte.
    *   `C31-C33`: Fabricación de muebles, otras manufacturas, reparación e instalación.
*   **Ramas Sectoriales Principales (Resto de la economía)**:
    *   `A`: Agricultura, ganadería, silvicultura y pesca.
    *   `B`: Industrias extractivas.
    *   `D`: Suministro de energía eléctrica, gas, vapor y aire acondicionado.
    *   `E`: Suministro de agua, saneamiento, gestión de residuos y descontaminación.
    *   `F`: Construcción.
    *   `G`: Comercio al por mayor y al por menor; reparación de vehículos de motor.
    *   `H`: Transporte y almacenamiento.
    *   `I`: Hostelería (servicios de alojamiento y comida).
    *   `J`: Información y comunicaciones.
    *   `K`: Actividades financieras y de seguros.
    *   `L`: Actividades inmobiliarias.
    *   `M`: Actividades profesionales, científicas y técnicas.
    *   `N`: Actividades administrativas y servicios auxiliares.
    *   `O`: Administración Pública y defensa; Seguridad Social obligatoria.
    *   `P`: Educación.
    *   `Q`: Actividades sanitarias y de servicios sociales.
    *   `R`: Actividades artísticas, recreativas y de entretenimiento.
    *   `S`: Otros servicios.
    *   `T`: Actividades de los hogares como empleadores.
    *   `U`: Actividades de organizaciones y organismos extraterritoriales.

### C. Metodología de Empalme del IPC del INE
Las series de IPC del INE presentan discontinuidades debidas al cambio periódico de la estructura de ponderaciones de la cesta de consumo (cambios de base). Para obtener una serie continua de variaciones logarítmicas de precios ($\Delta \ln P_{c,t}$), el código realiza un enlace informático entre dos bases de datos:
1.  **Serie Antigua (Base 1992)**: Extraída del archivo `269.xlsx` del INE, cubre el periodo de 1995 a 2001.
2.  **Serie Moderna (Base 2025)**: Extraída del archivo `76144.xlsx` del INE, abarca de 2002 a 2025.

El algoritmo de cálculo implementado en el script opera bajo las siguientes reglas algebraicas:
*   Para los años del periodo 1996-2001, la inflación se calcula como la diferencia logarítmica de los niveles medios anuales del IPC base 1992:
    $$\Delta \ln P_{c,y} = \ln(IPC\_old_y) - \ln(IPC\_old_{y-1})$$
*   Para el año 2002, año frontera entre ambas series donde el cociente directo de niveles introduciría un error de escala de varios órdenes de magnitud, se fuerza la tasa oficial media de inflación del INE para 2002 (3,5%):
    $$\Delta \ln P_{c,2002} = \ln(1 + 0,035)$$
*   Para los años del periodo 2003-2021, la inflación se calcula sobre la serie del IPC base 2025:
    $$\Delta \ln P_{c,y} = \ln(IPC\_new_y) - \ln(IPC\_new_{y-1})$$

Este vector de inflación en diferencias logarítmicas permite deflactar el crecimiento del salario nominal por hora de forma limpia.

---

## 4. Resultados cuantitativos acumulados (1996-2019)

El análisis del crecimiento acumulado de los salarios reales durante el ciclo pre-COVID (1996-2019) revela que el poder adquisitivo estructural en España apenas avanzó un **+4,84%** en todo el periodo (un exiguo +0,20% anual promedio). 

La descomposición exacta en puntos porcentuales del acumulado se detalla a continuación:

$$\text{Variación Salario Real (1996-2019)} = -6,50\% \ (\text{Participación Trabajo}) + 14,54\% \ (\text{Productividad Real}) - 3,20\% \ (\text{Cuña Precios}) = +4,84\%$$

A su vez, la contribución acumulada de la productividad real por hora (+14,54%) se descompone en:
*   Composición Laboral (Educación): **+9,57%**
*   Intensificación de Capital (TIC + no-TIC + Intangible): **+10,44%**
    *   Capital TIC: **+0,56%**
    *   Capital no-TIC: **+8,27%**
    *   Capital intangible: **+1,61%**
*   PTF intrasectorial (Eficiencia): **-12,30%**
*   Reasignación sectorial (*Between*): **+6,83%**

$$\text{Productividad Real} = +9,57\% \ (\text{Educación}) + 10,44\% \ (\text{Capital}) - 12,30\% \ (\text{PTF}) + 6,83\% \ (\text{Reasignación}) = +14,54\%$$

### Cómo interpretar los gráficos de contribuciones

En los gráficos generados por el proyecto, las contribuciones de los factores se representan mediante barras apiladas, donde cada color se asocia a un componente y el salario real total se muestra como una línea negra que recorre los años o etapas. 

*   **En el Gráfico Acumulado**: Las barras acumuladas para el periodo 1996-2019 muestran que el empuje positivo del capital humano (barra verde) y el capital físico tradicional (barra azul medio) se ven completamente neutralizados y absorbidos por la gran barra morada negativa que representa el desplome de la PTF intrasectorial (-12,30%). La línea negra (salario real neto) avanza apenas por encima de cero debido a este sumidero de eficiencia y a la caída de la participación laboral (barra roja terrosa).
*   **En el Gráfico de Etapas (Medias Anuales)**: Permite observar el cambio de dinámicas. En la etapa de la burbuja (1996-2007), la línea negra está plana debido a la coincidencia de una fuerte aportación negativa de la barra morada (PTF: -0,98% anual) con aportaciones positivas de la barra gris (reasignación sectorial: +0,89% anual). En la etapa de recuperación (2014-2019), la línea negra asciende a +0,75% anual gracias a que la barra de la PTF morada vuelve al terreno positivo (+0,30% anual) y la cuña de precios (barra ámbar) suma capacidad adquisitiva (+0,46% anual) por el abaratamiento de la energía importada.

---

## 5. Anatomía de la distorsión del COVID-19 (1996-2019 vs 1996-2021)

La comparación cuantitativa de la descomposición acumulada truncando la serie en 2019 frente a la serie completa que se extiende hasta 2021 revela una profunda discrepancia estadística:

| Variable de la Descomposición | Periodo Limpio (1996-2019) | Periodo con COVID (1996-2021) | Sesgo Estadístico (p.p.) |
| :--- | :---: | :---: | :---: |
| **Salario Real (Total)** | **+4,84%** | **+9,58%** | **+4,74** |
| **Participación del Trabajo ($s_L$)** | **-6,50%** | **-1,98%** | **+4,52** |
| **Productividad Laboral Real** | **+14,54%** | **+13,78%** | **-0,76** |
| _└─ Composición Laboral_ | _+9,57%_ | _+10,31%_ | _+0,74_ |
| _└─ Capital (TIC + no-TIC + Intang.)_ | _+10,44%_ | _+11,59%_ | _+1,15_ |
| _└─ PTF intrasectorial_ | _-12,30%_ | _-19,41%_ | _-7,11_ |
| _└─ Reasignación sectorial_ | _+6,83%_ | _+11,29%_ | _+4,46_ |
| **Cuña de Precios** | **-3,20%** | **-2,23%** | **+0,97** |

Desde la perspectiva contable y de contabilidad nacional, esta masiva distorsión en solo dos años se explica por tres fenómenos específicos de la pandemia:

### 1. El espejismo del reparto en la participación salarial
En 2020, el PIB real y nominal de España sufrió un desplome histórico superior al 10%. Sin embargo, la puesta en marcha de los esquemas de ERTE y ayudas públicas mantuvo las rentas salariales agregadas contables ($LAB_t$) en niveles muy estables en comparación con la caída de la producción. 
Contablemente, la participación laboral se define como:
$$s_{L,t} = \frac{LAB_t}{VA_t}$$
Al caer el VAB nominal ($VA_t$) en una proporción mucho mayor que las remuneraciones del trabajo ($LAB_t$), el ratio $s_{L,t}$ experimentó un aumento contable brusco y artificial en 2020. Al acumular los datos hasta 2021, este incremento transitorio enmascara la caída del poder de negociación estructural de los asalariados acumulado durante las dos décadas anteriores, reduciendo el lastre estimado de la participación salarial de un -6,50% a un -1,98%. Este aparente "mejor reparto de la renta" fue un artefacto del subsidio fiscal transitorio de los ERTEs, no una ganancia estructural.

### 2. El desplome artificial de la PTF sectorial como residuo
La PTF se calcula deduciendo de la variación de producción la variación del empleo y el capital. Durante el año de la pandemia, la producción colapsó debido a las restricciones físicas de actividad, pero el stock de capital (fábricas, locales, equipos) permaneció intacto y el número contable de trabajadores se mantuvo elevado en las plantillas (gracias a la protección del empleo de los ERTEs). 
Al no poder ajustarse los factores de producción en la misma medida en que cayó la producción física, la eficiencia estimada con la que se combinan los factores se desplomó. Matemáticamente, este shock de subutilización de la capacidad instalada fue absorbido en su totalidad por el residuo de la PTF, inflando la ineficiencia agregada de un -12,30% en 2019 a un -19,41% en 2021. Este desplome no representa un retroceso tecnológico de las empresas españolas, sino una parálisis legal de la producción.

### 3. El sesgo de selección en la reasignación sectorial (*between*)
Durante los confinamientos de 2020 y las restricciones de 2021, los sectores económicos de proximidad física y bajo valor añadido medio (hostelería, pequeño comercio, ocio) vieron colapsar sus horas de trabajo efectivas de forma drástica. Por contra, sectores intensivos en conocimiento y capaces de operar en teletrabajo (finanzas, informática, telecomunicaciones), que registran niveles de VAB por hora muy elevados, mantuvieron estable su actividad.
Este cambio composición de las horas trabajadas en la economía nacional provocó un salto matemático excepcional en el efecto reasignación, disparándolo de un +6,83% acumulado en 2019 a un +11,29% en 2021. Esta ganancia de productividad agregada no responde a una modernización estructural del modelo productivo (es decir, no es que el empleo se haya trasladado permanentemente a sectores tecnológicos), sino al cierre temporal selectivo de los sectores menos productivos del país.

---

## 6. Conclusión metodológica

La disección analítica de los datos de EUKLEMS e INTANProd subraya la importancia del rigor metodológico en la macroeconomía aplicada. La inclusión del bienio 2020-2021 introduce anomalías estadísticas severas derivadas del shock de la pandemia de COVID-19 y de los mecanismos públicos de estabilización de rentas. 

Contablemente, estas anomalías alteran los pesos y ratios macroeconómicos básicos de la contabilidad nacional. Por ello, el análisis estructurado del periodo 1996-2019 es el único procedimiento válido para obtener un diagnóstico limpio sobre las tendencias de fondo del modelo productivo español. Revela que el estancamiento de los salarios reales no es un mero problema coyuntural, sino el resultado matemático exacto de una ineficiencia persistente (PTF) que anula de forma continua el esfuerzo acumulado de capital humano e inversión empresarial física de las últimas décadas.

---

## Recursos y Transparencia

*   **Artículo publicado:** Una versión resumida y divulgativa de este análisis se publicó originalmente en *Cinco Días*: [¿Cómo se pueden explicar treinta años de estancamiento salarial?](https://cincodias.elpais.com/economia/2026-06-18/como-se-pueden-explicar-treinta-anos-de-estancamiento-salarial.html).
*   **Código y datos abiertos:** El código en Python utilizado para calcular esta descomposición macroeconómica y los ficheros asociados están disponibles públicamente. Puedes auditar o replicar el modelo visitando el directorio de este post en el repositorio del proyecto: [GitHub - Descomposición salarios reales](https://github.com/ProyectSubstrack/Substack/tree/main/Descomposici%C3%B3n%20salarios%20reales).

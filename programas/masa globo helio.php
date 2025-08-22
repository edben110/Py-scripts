<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Función para convertir grados a radianes
    function degToRad($degrees) {
        return $degrees * (pi() / 180);
    }

    // Función para calcular el volumen del globo
    function calcularVolumenGlobo($radio) {
        return (4/3) * pi() * pow($radio, 3);
    }

    // Función para calcular la masa del helio en el globo
    function calcularMasaHelio($volumen, $densidad_helio) {
        return $densidad_helio * $volumen;
    }

    // Función para calcular la fuerza de flotación
    function calcularFuerzaFlotacion($densidad_aire, $volumen, $g) {
        return $densidad_aire * $volumen * $g;
    }

    // Función para calcular la carga eléctrica
    function calcularCargaElectrica($peso, $theta, $distancia_m, $ke) {
        $fuerza_electrostatica = $peso * tan($theta);
        return sqrt($fuerza_electrostatica * pow($distancia_m, 2) / $ke);
    }

    // Obtener entradas del formulario
    $circunferencia_globo = floatval($_POST['circunferencia_globo']);
    $masa_globo_desinflado = floatval($_POST['masa_globo_desinflado']);
    $masa_cuerda_experimental = floatval($_POST['masa_cuerda_experimental']);
    $distancia = floatval($_POST['distancia']);
    $theta = degToRad(floatval($_POST['theta']));

    // Constantes
    $ke = 9 * pow(10, 9); // Constante de Coulomb (N·m²/C²)
    $densidad_aire = 1.225; // Densidad del aire en kg/m³
    $densidad_elemento_globo = 0.1785; // Densidad del helio en kg/m³
    $g = 9.81; // Aceleración de la gravedad en m/s²

    // Cálculo del radio y volumen del globo
    $radio_globo = $circunferencia_globo / (2 * pi());
    $radio_globo_m = $radio_globo / 100;
    $volumen_globo = calcularVolumenGlobo($radio_globo_m);
    $masa_helio = calcularMasaHelio($volumen_globo, $densidad_elemento_globo);
    $masa_globo = $volumen_globo * $densidad_elemento_globo;

    // Cálculo de fuerzas
    $fuerza_flotacion = calcularFuerzaFlotacion($densidad_aire, $volumen_globo, $g);
    $peso_globo = ($masa_helio + ($masa_globo_desinflado / 1000)) * $g;
    $peso_cuerda = $fuerza_flotacion - $peso_globo;
    $masa_cuerda = ($peso_cuerda / $g) * 1000;

    // Cálculo de la aceleración del globo
    $fuerza_empuje = ($densidad_aire - $densidad_elemento_globo) * $volumen_globo * $g;
    $masa_total = ($masa_globo_desinflado / 1000) + $masa_helio;
    $fuerza_neta = $fuerza_empuje - ($masa_total * $g);
    $aceleracion_globo = $fuerza_neta / $masa_total;

    // Cálculo del error absoluto
    $error_absoluto = abs((($masa_cuerda - $masa_cuerda_experimental) / $masa_cuerda) * 100);

    // Cálculo de la carga eléctrica
    $peso = $masa_globo * $g;
    $distancia_m = $distancia / 100;
    $carga_electrica = calcularCargaElectrica($peso, $theta, $distancia_m, $ke);
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cálculo del Globo</title>
</head>
<body>
    <form method="post">
        <label>Circunferencia del globo (cm): <input type="number" step="any" name="circunferencia_globo" required></label><br>
        <label>Masa del globo desinflado (g): <input type="number" step="any" name="masa_globo_desinflado" required></label><br>
        <label>Masa experimental de la cuerda (g): <input type="number" step="any" name="masa_cuerda_experimental" required></label><br>
        <label>Distancia entre globos (cm): <input type="number" step="any" name="distancia" required></label><br>
        <label>Ángulo de inclinación (°): <input type="number" step="any" name="theta" required></label><br>
        <button type="submit">Calcular</button>
    </form>

    <?php if ($_SERVER["REQUEST_METHOD"] == "POST"): ?>
        <h2>Resultados:</h2>
        <p>El porcentaje de error es de <?= number_format($error_absoluto, 2) ?>%</p>
        <p>La masa de la cuerda es aproximadamente <?= number_format($masa_cuerda, 2) ?> gramos</p>
        <p>La fuerza de empuje del globo al ser soltado es aproximadamente <?= number_format($fuerza_empuje, 2) ?> N</p>
        <p>La aceleración del globo al ser soltado es aproximadamente <?= number_format($aceleracion_globo, 2) ?> m/s²</p>
        <p>La carga eléctrica experimental es de <?= sprintf("%.2e", $carga_electrica) ?> C</p>
    <?php endif; ?>
</body>
</html>

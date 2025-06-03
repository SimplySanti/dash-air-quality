import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H1('Recursos Utilizados Para Este Estudio'),
    html.P(
        className='secondaryText',
        children=['Los datos presentados en este dashboard provienen de estaciones de monitoreo ambiental ubicadas en distintos puntos estratégicos de la zona metropolitana de Monterrey, Nuevo León. Estas estaciones recolectan información en tiempo real sobre diversos contaminantes atmosféricos, tales como partículas PM2.5, PM10, ozono (O₃), dióxido de nitrógeno (NO₂), dióxido de azufre (SO₂) y monóxido de carbono (CO). La infraestructura de monitoreo es operada por organismos oficiales y complementada, en algunos casos, con sensores independientes instalados para fines de investigación. La decisión de compartir públicamente estos datos responde a un compromiso con la transparencia, la ciencia abierta y la colaboración interdisciplinaria. Al poner esta información a disposición de la comunidad académica, centros de investigación y universidades, buscamos fomentar el desarrollo de nuevos proyectos que contribuyan a una comprensión más profunda de la calidad del aire en la región. Asimismo, se espera que esta iniciativa sirva como base para propuestas de mejora en políticas públicas, estrategias de mitigación y soluciones tecnológicas enfocadas en el bienestar ambiental y la salud de la población.']
    ),
    html.Div(
        style={
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'space-between',
            'marginTop': '40px'
        },
        children=[
            html.A(
                "Registros de Aire Nuevo León",
                href="/assets/registros_airenuevoleon.xlsx",
                download="registros_airenuevoleon.xlsxf",
                style={
                    'border': '2px solid black',
                    'borderRadius': '8px',
                    'width': '30%',
                    'height': '120px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'textDecoration': 'none',
                    'color': 'black',
                    'fontWeight': 'bold'
                }
            ),
            html.A(
                "Sensores de Aire Nuevo León",
                href="/assets/sensores_airenuevoleon.xlsx",
                download="sensores_airenuevoleon.pdf",
                style={
                    'border': '2px solid black',
                    'borderRadius': '8px',
                    'width': '30%',
                    'height': '120px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'textDecoration': 'none',
                    'color': 'black',
                    'fontWeight': 'bold'
                }
            ),
            html.A(
                "Descargar Estudio Detallado",
                href="/assets/TODO",
                download="TODO.pdf",
                style={
                    'border': '2px solid black',
                    'borderRadius': '8px',
                    'width': '30%',
                    'height': '120px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'textDecoration': 'none',
                    'color': 'black',
                    'fontWeight': 'bold'
                }
            ),
        ]
    )
])
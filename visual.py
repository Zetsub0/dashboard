import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split


# Чтение входных обобщенных данных и кластеризованных данных (region_vectors_output_3, region_vectors_output_4)
roads_df = pd.read_csv('region_roads.csv', sep=',')
reg_vec_df = pd.read_csv('region_vectors.csv', sep=',')
regions_3clust_df = pd.read_csv('region_vectors_output_3.csv', sep=',')
regions_4clust_df = pd.read_csv('region_vectors_output_4.csv', sep=',')


reg_options = []

roads_names = ['Биомедицина', 'Нанотехнологии, композиты, пр.', 'Аэрокосмос', 'Сельское хозяйство', 'Информационные технологии', 'Другое', 'Вовлечение молодeжи в работу средств массовой информации', 'Работа с молодeжью, находящейся в социально-опасном положении', 'Творческая деятельность', 'Формирование у молодeжи семейных ценностей', 'Волонтeрская деятельность', 'Здоровый образ жизни и занятия спортом, культура безопасности']

nums_regions = median_excel_data = pd.read_excel('reg.xlsx', index_col=None, header=None)

for row in nums_regions.iterrows():
	reg_options.append({'label': row[1].tolist()[1].replace('\xa0', ' '), 'value': row[1].tolist()[0]})


# Инициализация веб-сервера
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True


# Универсальная функция визуализации кластеров по пользовательским параметрам
def clusters_show_2d(x_col, y_col, clusters_count=4, scale=0.9):
	markers = ['ro', 'go', 'bo', 'yo', 'co', 'mo', 'ko']
	dfs = []

	for i in range(clusters_count):    

		x = np.array(regions_4clust_df[(regions_4clust_df['k_means_clust'] == i)][x_col])
		y = np.array(regions_4clust_df[(regions_4clust_df['k_means_clust'] == i)][y_col])

		#_, x, _, y = train_test_split(x, y, test_size=scale, random_state=1)

		dfs.append(pd.DataFrame({'name': 'Кластер ' + str(i + 1), 'color': [markers[i] for j in range(len(x))], 'x': x, 'y': y}))

	_df = pd.concat(dfs)
	fig = px.scatter(_df, x='x', y='y', color='name', labels={'x': x_col, 'y': y_col})

	return fig


# метаданные
SIDESTYLE = {
	'position': 'fixed',
	'top': 0,
	'left': 0,
	'bottom': 0,
	'width': '16rem',
	'padding': '2rem 1rem',
	'background-color': '#222222',
}


CONTSTYLE = {
	'margin-left': '18rem',
	'margin-right': '2rem',
	'padding': '2rem 1rem',
}


# Фронтэнд. Структура. Боковое меню
app.layout = html.Div([
	dcc.Location(id='url'),
	html.Div(
		[
			html.H2('AI4H', className='display-3', style={'color': 'white'}),
			html.Hr(style={'color': 'white'}),
			dbc.Nav(
				[
					dbc.NavLink('Краткая характеристика регионов, общие показатели', href='/page1', active='exact'),
					dbc.NavLink('Визуализация кластеров по параметрам', href='/page2', active='exact'),
				],
				vertical=True,pills=True),
		],
		style=SIDESTYLE,
	),
	html.Div(id='page-content', children=[], style=CONTSTYLE)
])


# Верстка первой страницы
@app.callback(
	Output('page-content', 'children'),
	[Input('url', 'pathname')])

def pagecontent(pathname):
	if pathname == '/page1':
		return [

			html.Div(
				children=[
					html.H1(children='Общая характеристика регионов', className='header-title'),
				], className='header'),

			html.P("Регион:"),
			dcc.Dropdown(id='page1_region',
				options=reg_options,
				value=2, className='dropdown', style= {'margin-bottom':'16px'}
			),
			html.Div(id='page1_reg_charac'), html.P("Тип диаграммы:"),
			dcc.Dropdown(id='page1_type_graph',
				options=[{'label': 'Круговая диаграмма', 'value': 'pie'},
						{'label': 'Столбчатая диаграмма', 'value': 'vertical'}],
				value='pie', style= {'margin-bottom':'16px'}
			), dcc.Graph(id='output_graph', style= {'margin-bottom':'64px'})
			]

	
# Верстка второй страницы	
	elif pathname == '/page2':
		return [
			html.Div(
				children=[
					html.H1(children='Визуализация данных', className='header-title'),

					html.P(children='Визуализация полученных данных в виде кластеров', className='header-description')
				], className='header'),

			html.Div([
				dcc.Dropdown(
					id='page3_drop',
					options=[
						{'label': 'Количество грантов', 'value': 'amount_grant'},
						{'label': 'Общий бюджет грантов', 'value': 'budget_grant_reg'},
						{'label': 'Бюджет региона', 'value': 'budget_reg'},
						{'label': 'Бюджет, выделенный на молодежные политики', 'value': 'budget2youth_reg'},
						{'label': 'Кол-во добровольцев по направлениям молодежных политик', 'value': 'volontiers_amount_reg'},
						{'label': 'Уникальные пользователи интернет-ресурсов молодежных направлений', 'value': 'uniq_users'},
						{'label': 'Бюджет, выделенный на маркетинг молодежных политик', 'value': 'budget_marketing'},
						{'label': 'Количество маркетинговых единиц (новостей, статей, постов и тд.)', 'value': 'marketing_units'},
						{'label': 'Численность региона', 'value': 'population'},
					],
					multi=True, value=['volontiers_amount_reg', 'budget2youth_reg'], className='dropdown', style={'margin-bottom':'32px'}
				), dcc.Graph(id='output3_graph')], className='card')

				]


# Передача данных для первой страницы
@app.callback(
	Output(component_id='output_graph', component_property='figure'),
	[Input(component_id='page1_region', component_property='value'), 
	Input("page1_type_graph", "value")]
)

def update_output(region, type_gpaph):
	data = roads_df[roads_df['code'] == region].iloc[0]
	if type_gpaph == 'vertical':
		figure = {
				'data': [
					{'x': roads_names, 'y': data.tolist()[3:], 'type': 'bar', 'name': 'Кластер №1'},],
				'layout': {
					'title': 'Доля бюджета по направлениям молодежной политики'
				}
			}
	elif type_gpaph == 'pie':
		figure = px.pie(data, values=data.tolist()[3:], names=roads_names, hole=.3)

	return figure


@app.callback(
	Output(component_id='page1_reg_charac', component_property='children'),
	[Input(component_id='page1_region', component_property='value')]
)

def update_output(value):
	data = reg_vec_df[reg_vec_df['code'] == value].iloc[0].tolist()

	charac_div = html.Div([
		html.P(children='Краткая характеристика региона: ' + data[0], className='header-description', style={'margin-bottom': '8px'}),
		html.P(children='Количество средств на человека в рамках проведения мероприятий по направлениям молодежной политики: {:.2f} руб./участника'.format(data[5]/data[6]), className='header-description', style={'margin-bottom': '8px'}),
		html.P(children='Отношение бюджета, выделяемого на направления молодежной политики, к общему бюджету региона: {:.6f}'.format(data[5]/data[4]), className='header-description', style={'margin-bottom': '8px'}),
		html.P(children='Отношение количества граждан, вовлеченных в добровольческую деятельность, к общему населению региона: {:.4f}'.format(data[12]/data[11]), className='header-description', style={'margin-bottom': '8px'}),
		html.P(children='Процентное соотношение добровольцев из школ/СПО/ВУЗов: ', className='header-description', style={'margin-bottom': '8px'}),
		dcc.Graph(figure=px.pie(data, values=[data[13], data[14], data[15]], names=['Школы', 'СПО', 'ВУЗы'], hole=.3)),

		], style={'margin-top': '32px', 'margin-bottom': '32px'
		})

	return charac_div


# Передача данных для второй страницы
@app.callback(
	Output(component_id='output3_graph', component_property='figure'),
	[Input(component_id='page3_drop', component_property='value')]
)

def update_output(value):

	return clusters_show_2d(value[0], value[1])



# Запуск веб-сервера
app.run_server(debug=True, port=3000)





































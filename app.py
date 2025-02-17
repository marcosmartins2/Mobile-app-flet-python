import flet as ft
import requests


API_BASE_URL = "http://localhost:8000/api"

def main(page:ft.Page):
    page.title = "exemplo"

    nome_field = ft.TextField(label="Nome")
    email_field = ft.TextField(label="Email")
    faixa_field = ft.TextField(label="Faixa")
    data_nascimento_field = ft.TextField(label="Data de nascimento (YYYY-MM-DD)")
    create_result = ft.Text()

    #Criar aluno aba 
    def criar_aluno_click(e):
        payload = {
            "nome":nome_field.value,
            "email":email_field.value,
            "faixa":faixa_field.value,
            "data_nascimento":data_nascimento_field.value
        }

        response = requests.post(API_BASE_URL+ '/',json=payload)

        if response.status_code == 200:
            aluno = response.json()
            create_result.value = f"Aluno criado:{aluno}"

        else:
            create_result.value = f"Erro: {response.text}"

        page.update()
    create_button = ft.ElevatedButton(text="Criar aluno",on_click=criar_aluno_click)


    criar_aluno_tab = ft.Column(
        [
            nome_field,
            email_field,
            faixa_field,
            data_nascimento_field,
            create_result, 
            create_button
        ],
        scroll=True
    )

    #listar aluno aba

    student_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('Nome')),
            ft.DataColumn(ft.Text('Email')),
            ft.DataColumn(ft.Text('Faixa')),
            ft.DataColumn(ft.Text('Data Nascimento')),
                 
                 ],rows=[]
    )

    list_result = ft.Text()

    def listar_alunos_click(e):
        response = requests.get(API_BASE_URL+'/aluno/')

        alunos = response.json()

        student_table.rows.clear()
        for aluno in alunos:
            row =ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(aluno.get('nome'))),
                    ft.DataCell(ft.Text(aluno.get('email'))),
                    ft.DataCell(ft.Text(aluno.get('faixa'))),
                    ft.DataCell(ft.Text(aluno.get('data_nascimento')))
                ]
            )
            student_table.rows.append(row)
        list_result.value = f"{len(alunos)} alunos encontrados"

        page.update()

    list_button = ft.ElevatedButton(text="Listar Alunos",on_click=listar_alunos_click)
    listar_aluno_tab = ft.Column([student_table,list_result,list_button],scroll=True)

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Criar aluno",content=criar_aluno_tab),
            ft.Tab(text="Listar alunos",content=listar_aluno_tab)
        ]
    )

    page.add(tabs)

if __name__ == "__main__":
    ft.app(target=main)




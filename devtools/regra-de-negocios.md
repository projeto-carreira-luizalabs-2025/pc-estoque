# Regras - CRUD de Estoque

## 📌 Escopo

Implementar um módulo de **controle de estoque** para os produtos cadastrados no catálogo da aplicação. Este módulo deve permitir o registro, atualização, consulta e exclusão da quantidade disponível em estoque para cada produto.

A identificação dos produtos no estoque será feita pela **mesma chave** utilizada no catálogo **(sku) de produtos** e na identidade **(seller_id)** do seller. A quantidade deve ser sempre registrada como **um valor inteiro**.

## 📌 Contexto

Faremos a implementação de um sistema para o controle de estoque, atraves de um projeto FastApi utilizando como padrão de retorno Rest.

O módulo de Estoque irá:

- Permitir o controle da quantidade disponível de cada produto.
- Restringir a quantidade informada a números inteiros.
- Disponibilizar operações CRUD para gestão de estoque:
  - **Create**: Registrar a quantidade inicial de um produto.
  - **Read**: Consultar a quantidade atual em estoque.
  - **Update**: Atualizar a quantidade de um produto em estoque.
  - **Delete**: Remover o registro de estoque de um produto.

## 📌 **Exemplo de estrutura de dados no Estoque:**

```json
{
  "seller_id": "LuizaLabs",
  "sku": "PROD01",
  "quantidade": 100
}
```

## 📌 Critérios de Aceite

- CREATE:
  - A quantidade deve obrigatoriamente ser um **valor inteiro positivo ou zero**.
  - A API deve validar e caso a quantidade informada não seja um valor inteiro, retorna uma mensagem de erro “Quantidade informada deve ser um número inteiro”
  - Retorna a mensagem de sucesso: “Registro criado com sucesso”
  - O sistema deve permitir cadastrar a quantidade inicial de um produto no estoque, associada ao seu `seller` e `sku`.
- UPDATE:
  - A quantidade deve obrigatoriamente ser um **valor inteiro positivo ou zero**.
  - A API deve validar e caso a quantidade informada não seja um valor inteiro, retorna uma mensagem de erro: “Quantidade informada deve ser um número inteiro”
  - Deve ser possível atualizar a quantidade em estoque de um produto existente.
  - Retorna a mensagem de sucesso: “Registro atualizado com sucesso”
  - Retorna um alerta caso a atualização deixe o estoque com as quantudades negativas, mensagem: “A quantidade no estoque não pode ser inferior a zero”
- DELETE:
  - Deve ser possível remover o registro de estoque de um produto.
  - Retorna a mensagem de sucesso: “Registro deletado com sucesso”
  - Retorna a mensagem de erro : “Registro não encontrado”
- READ:
  - Deve ser possível consultar a quantidade atual de qualquer produto informando seu `seller` e/ou seu `sku`.
  - Mostar os resultados das buscas de forma paginadas.

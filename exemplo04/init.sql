CREATE TABLE vendas (
    id SERIAL PRIMARY KEY,
    data_venda DATE NOT NULL,
    produto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    quantidade INT NOT NULL
);

INSERT INTO vendas (data_venda, produto, categoria, valor, quantidade)
VALUES 
  ('2025-01-15', 'Xbox Series S', 'Console', 1970.00, 45),
  ('2025-01-20', 'Xbox Game Pass', 'Assinatura', 120.00, 50),
  ('2025-02-05', 'PS5', 'Console', 3200.00, 15),
  ('2025-01-15', 'PS Plus', 'Assinatura', 95.00, 425),
  ('2025-01-23', 'Nintendo Switch', 'Console', 1970.00, 105),
  ('2025-01-23', 'Controle  PS5', 'Acessórios', 500, 65),
  ('2025-01-23', 'Headset Gamer', 'Acessórios', 350, 21);
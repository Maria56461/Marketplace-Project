Maria-Alexandra Barbu, 335CA
Arhitectura Sistemelor de Calcul
Tema 1- Marketplace
-----------------------------------------------------------------------------------

Mi-am organizat datele astfel:
- un dictionar in care am stocat elemente de tipul id_producer:number_of_products
- un dictionar in care am stocat elemente de tipul
id_producer:[product1, product2,...] (producerId and its list of products)
- un dictionar in care am stocat elemente de tipul
id_cart:[(idproducer1, product1), (idproducer2, product2), etc] (the cart_id and the
list of products in the cart along with the producer of each product)

Am folosit 4 Lock-uri pentru a evita accesul simultan asupra unei variabile de catre
mai multe thread-uri: cate un Lock pentru metodele add_to_cart si remove_from_cart,
si cate un Lock pentru metodele new_cart si register_producer.
Pentru generare de id-uri unice am folosit functia din python uuid4().

Flow-ul programului:
Producatorul cu propriul sau id publica pe rand produsele sale, asteptand dupa fiecare
publicatie un timp corespunzator produsului. Daca nu poate publica fiindca si-a
indeplinit numarul maxim de produse acceptate, producatorul va trebui sa astepteun timp
mai lung numit republish_wait_time.
Consumatorul genereaza un id pentru fiecare cos al sau si, pentru fiecare element din
cos, analizeaza tipul operatiei care trebuie efectuata, add sau remove. Daca vreuna
dintre operatii intoarce False, atunci consumatorul asteapta retry_wait_time. Consumatorul
plaseaza o comanda afisand lista de produse din cos.
Am implementat si partea de Unittesting, generand cate un test pentru fiecare metoda din
clasa Marketplace.
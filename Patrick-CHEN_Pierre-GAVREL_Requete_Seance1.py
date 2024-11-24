import sqlite3
import pandas

# Création de la connexion
conn = sqlite3.connect("E:/BUT3/NoSQL/seance1/ClassicModel.sqlite")

# Requête qui liste les clients de la base de données, on trouve les entreprises : Havel & Zbyszek Co, American Souvenirs Inc, etc
question1 = pandas.DataFrame(pandas.read_sql_query("SELECT C.CustomerNumber, C.customerName FROM Customers C LEFT OUTER JOIN Orders O Using(customerNumber) WHERE O.orderDate IS NULL;", conn))

# Pour chaque employé on a son nombre de clients, le nombre de commandes et le montant total. Diana, Mary, Jeff ou encore William n'ont pas de clients, ni de commandes donc un montant total à 0.
question2 = pandas.DataFrame(pandas.read_sql_query(
    """
    SELECT E.employeeNumber, E.FirstName, E.LastName, count(distinct(C.customerNumber)), count(O.orderNumber), sum(P.amount)
    FROM Employees E left outer join Customers C ON E.employeeNumber = C.SalesRepEmployeeNumber
    left outer join Orders O ON C.customerNumber = O.customerNumber
    left outer join Payments P ON O.customerNumber = P.customerNumber
    GROUP BY E.employeeNumber;""", conn))

# Pour chaque bureau on a son nombre de clients, de commandes et le montant total et le nombre de clients étrangés. On voit que le bureau 1 situé à San Francisco a 12 clients, 48 commandes, un montant total de plus de 13 millions et 0 clients étrangés.
question3 = pandas.DataFrame(pandas.read_sql_query(
    """
    SELECT O.officeCode, O.city, O.country, count(distinct C.customerNumber), count(distinct Od.orderNumber), sum(P.amount), count(distinct
    case when C.country != O.country then C.customerNumber else null end)
    from offices O left join employees E ON O.officecode = E.officecode
    left join customers C ON C.salesrepemployeenumber = E.employeeNumber
    left join orders Od ON Od.customerNumber = C.customerNumber
    left join payments P ON P.customerNumber = C.customerNumber
    group by O.officecode, O.city, O.country;""", conn))

# Pour chaque produit on a son nombre de commandes, la quantité commandée et le nombre de clients différents qui l'ont commandé. Par exemple, on a pour le modèle 1969 Harley Davidson Ultimate Chopper, il se retrouve dans 28 commandes, il a été commandé 1026 fois par 26 clients différents.
question4 = pandas.DataFrame(pandas.read_sql_query(
    """
    select products.productCode, products.productName,count(distinct(orderdetails.orderNumber)), sum(orderdetails.quantityOrdered), count(distinct(customers.customernumber))
    from products left join orderdetails ON products.productcode = orderdetails.productcode
    left join orders ON orderdetails.ordernumber = orders.ordernumber
    left join customers ON orders.customernumber = customers.customernumber
    group by products.productcode;""", conn))

# Pour chaque pays on a le nombre de commandes, le montant total des commandes et le montant total payé. Par exemple, les clients en Australie ont fait 19 commandes, pour un montant total de 2182269.38 et un montant total payé de près de 24825410.
question5 = pandas.DataFrame(pandas.read_sql_query(
    """
    select C.country, count(distinct O.orderNumber), sum(OD.quantityordered * OD.priceeach), sum(P.amount)
    from customers C left join Orders O ON O.customerNumber = C.customerNumber
    left join Orderdetails OD ON OD.orderNumber = O.orderNumber
    left join Payments P ON P.customerNumber = C.customerNumber
    GROUP BY 1;""", conn))

# Tableau de contingence du nombre de commande entre la ligne de produits et le pays du client. Par exmeple, on voit que la catégorie de produit Classic Cars s'est retrouvé dans 12 commandes faites en Australie.
question6 = pandas.DataFrame(pandas.read_sql_query(
    """
    select P.productline, C.country, count(distinct O.ordernumber)
    from Products P
    left join orderdetails OD on OD.productCode=P.productCode
    left join Orders O on O.orderNumber=OD.orderNumber
    left join customers C on C.customernumber=O.customernumber
    group by P.productline, C.country;
    """, conn))

# Tableau de contingence du montant total payé entre la ligne de produits et le pays. Par exemple, on voit que le montant total des commandes de la catégorie CLassic Cars en Australie est de 7504795.97
question7 = pandas.DataFrame(pandas.read_sql_query(
    """
    select P.productline, C.country, sum(Pa.amount)
    from Products P
    left join orderdetails OD on OD.productCode=P.productCode
    left join Orders O on O.orderNumber=OD.orderNumber
    left join customers C on C.customernumber=O.customernumber
    left join payments Pa on Pa.customernumber=C.customernumber
    group by P.productline, C.country;
    """, conn))

# Top 10 des produits pour lequels la marge moyenne est la plus importante. Par exemple, 1952 Alpine Renault 1300 a la meilleure marge moyenne avec 99.006429
question8 = pandas.DataFrame(pandas.read_sql_query(
    """
    select P.productCode, P.productName, avg(priceeach-buyprice)
    from orderdetails OD
    inner join products P on P.productcode=OD.productcode
    group by P.productCode
    order by 3 desc
    limit 10;
    """, conn))

# Liste des produits qui ont été vendu à perte par les clients. Par exemple, le produit 1962 LanciaA Delta 16V a été acheté à 103.42 et est vendu à 61.99 unité par le client Online Diecast Creations Co.
question9 = pandas.DataFrame(pandas.read_sql_query(
    """
    select OD.productcode, O.customernumber, priceeach, buyprice
    from orderdetails OD
    inner join products P on P.productcode=OD.productcode
    inner join orders O on O.ordernumber=OD.ordernumber
    where priceeach-buyprice < 0;
    """, conn))

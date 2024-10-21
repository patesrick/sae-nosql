import sqlite3
import pandas

# Création de la connexion
conn = sqlite3.connect("E:/BUT3/NoSQL/seance1/ClassicModel.sqlite")

question1 = pandas.DataFrame(pandas.read_sql_query("SELECT C.CustomerNumber, C.customerName FROM Customers C LEFT OUTER JOIN Orders O Using(customerNumber) WHERE O.orderDate IS NULL;", conn))

question2 = pandas.DataFrame(pandas.read_sql_query(
    """
    SELECT E.employeeNumber, E.FirstName, E.LastName, count(distinct(C.customerNumber)), count(O.orderNumber), sum(P.amount)
    FROM Employees E left outer join Customers C ON E.employeeNumber = C.SalesRepEmployeeNumber
    left outer join Orders O ON C.customerNumber = O.customerNumber
    left outer join Payments P ON O.customerNumber = P.customerNumber
    GROUP BY E.employeeNumber;""", conn))

question3 = pandas.DataFrame(pandas.read_sql_query(
    """
    SELECT O.officeCode, O.city, O.country, count(distinct C.customerNumber), count(distinct Od.orderNumber), sum(P.amount), count(distinct
    case when C.country != O.country then C.customerNumber else null end)
    from offices O left join employees E ON O.officecode = E.officecode
    left join customers C ON C.salesrepemployeenumber = E.employeeNumber
    left join orders Od ON Od.customerNumber = C.customerNumber
    left join payments P ON P.customerNumber = C.customerNumber
    group by O.officecode, O.city, O.country;""", conn))

question4 = pandas.DataFrame(pandas.read_sql_query(
    """
    select products.productCode, products.productName,count(distinct(orderdetails.orderNumber)), sum(orderdetails.quantityOrdered), count(distinct(customers.customernumber))
    from products left join orderdetails ON products.productcode = orderdetails.productcode
    left join orders ON orderdetails.ordernumber = orders.ordernumber
    left join customers ON orders.customernumber = customers.customernumber
    group by products.productcode;""", conn))

question5 = pandas.DataFrame(pandas.read_sql_query(
    """
    select C.country, count(distinct O.orderNumber), sum(OD.quantityordered * OD.priceeach), sum(P.amount)
    from customers C left join Orders O ON O.customerNumber = C.customerNumber
    left join Orderdetails OD ON OD.orderNumber = O.orderNumber
    left join Payments P ON P.customerNumber = C.customerNumber
    GROUP BY 1;""", conn))

question6 = pandas.DataFrame(pandas.read_sql_query(
    """
    select P.productline, C.country, count(distinct O.ordernumber)
    from Products P
    left join orderdetails OD on OD.productCode=P.productCode
    left join Orders O on O.orderNumber=OD.orderNumber
    left join customers C on C.customernumber=O.customernumber
    group by P.productline, C.country;
    """, conn))

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

question8 = pandas.DataFrame(pandas.read_sql_query(
    """
    select P.productCode, P.productName, avg(priceeach-buyprice)
    from orderdetails OD
    inner join products P on P.productcode=OD.productcode
    group by P.productCode
    order by 3 desc
    limit 10;
    """, conn))
    
question9 = pandas.DataFrame(pandas.read_sql_query(
    """
    select OD.productcode, O.customernumber, priceeach, buyprice
    from orderdetails OD
    inner join products P on P.productcode=OD.productcode
    inner join orders O on O.ordernumber=OD.ordernumber
    where priceeach-buyprice < 0;
    """, conn))
UPDATE Quantity 
SET name = substr(SUBSTR(name, name,length(name)-2),3,length(name));
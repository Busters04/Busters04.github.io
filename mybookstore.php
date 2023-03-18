<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello World</title>
</head>
<body>
    <?php 
        $connection = mysqli_connect("localhost", "root", "X1*aEW17lmtq%,**", "mybookstore");
        if(!$connection){
            die("could not connect".mysql_connect_error());
        }

        $query = "select * from author_info";

        $stmt = mysqli_query($connection,$query);

        while($row = mysqli_fetch_array($stmt,MYSQLI_ASSOC)){
            echo $row['author_fname']." ".$row['author_lname'].'</br>';
        }
     ?>
</body>
</html>
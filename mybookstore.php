<?php
    $connection = mysqli_connect("localhost", "root", "X1*aEW17lmtq%,**", "mybookstore");
    if(!$connection){
        die("could not connect".mysql_connect_error());
    }

    $sql = "SELECT author_id, author_fname, author_lname, author_country FROM author_info WHERE author_id > 5";

    $result = mysqli_query($connection, $sql);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Book Store</title>
</head>
<body>
    <table align="center" border="1px" style="width:600px; line-height:40px;">
        <tr>
            <th colspan="4"><h2>Authors</h2></th>
        </tr>
        <t>
            <th> ID </th>
            <th> First Name </th>
            <th> Last Name </th>
            <th> Country </th>
        </t>

    <?php 
        while($rows = mysqli_fetch_assoc($result)){
    ?>
        <tr>
            <td><?php echo $rows['author_id'].' '; ?></td>
            <td><?php echo $rows['author_fname'].' '; ?></td>
            <td><?php echo $rows['author_lname'].' '; ?></td>
            <td><?php echo $rows['author_country'].'<br>'; ?></td>
        </tr>
    <?php    
        }
     ?>
     </table>
</body>
</html>
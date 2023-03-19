<?php
    $connection = mysqli_connect("localhost", "root", "X1*aEW17lmtq%,**", "mybookstore");
    if(!$connection){
        die("could not connect".mysql_connect_error());
    }

    $sql = "SELECT * FROM author_info WHERE author_id != 0";

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
    <table align="center" border="1px" style="width:500px; line-height:40px;">
        <tr>
            <th colspan="2"><h2> All Authors</h2></th>
        </tr>
        <t>
            <th> Author Name </th>
            <th> Author Country </th>
        </t>

    <?php 
        while($rows = mysqli_fetch_assoc($result)){
    ?>
        <tr>
            <td style="text-align:center"><?php echo $rows['author_fname'].' '.$rows['author_lname']; ?></td>
            <td style="text-align:center"><?php echo $rows['author_country'].'<br>'; ?></td>
        </tr>
    <?php    
        }
     ?>
     </table>
</body>
</html>
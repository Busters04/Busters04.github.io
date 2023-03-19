<?php
    $connection = mysqli_connect("localhost", "root", "X1*aEW17lmtq%,**", "mybookstore");
    if(!$connection){
        die("could not connect".mysql_connect_error());
    }

    $sql = "SELECT * FROM book_info WHERE book_id != 0";

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
    <table align="center" border="1px" style="width:1000px; line-height:40px;">
        <tr>
            <th colspan="6"><h2> All Books</h2></th>
        </tr>
        <t>
            <th> Book Title </th>
            <th> Book Genre </th>
            <th> Publisher's Name </th>
            <th> Year Published </th>
            <th> ISBN Number </th>
            <th> Cost of Book </th>
        </t>

    <?php 
        while($rows = mysqli_fetch_assoc($result)){
    ?>
        <tr>
            <td style="text-align:center"><?php echo $rows['book_title']; ?></td>
            <td style="text-align:center"><?php echo $rows['book_genre']; ?></td>
            <td style="text-align:center"><?php echo $rows['publisher_name']; ?></td>
            <td style="text-align:center"><?php echo $rows['year_published']; ?></td>
            <td style="text-align:center"><?php echo $rows['ISBN']; ?></td>
            <td style="text-align:center"><?php echo $rows['book_cost'].'<br>'; ?></td>
        </tr>
    <?php    
        }
     ?>
     </table>
</body>
</html>
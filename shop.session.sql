SELECT *
FROM users as u
    INNER JOIN orders as o ON u.id = o.user_id
ORDER BY o.user_id;
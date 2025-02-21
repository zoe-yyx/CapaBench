theory TreeReverseInj
  imports Main
begin

datatype tree = Leaf | Node tree int tree

fun tree_reverse :: "tree \<Rightarrow> tree" where
  "tree_reverse Leaf = Leaf"
| "tree_reverse (Node l v r) = Node (tree_reverse r) v (tree_reverse l)"

lemma tree_reverse_inj: "tree_reverse t1 = tree_reverse t2 \<Longrightarrow> t1 = t2"
proof (induction t1 arbitrary: t2)
  case Leaf
  then have "tree_reverse t2 = Leaf" by simp
  thus ?case
  proof (cases t2)
    case Leaf
    then show ?thesis by simp
  next
    case (Node l v r)
    then have "tree_reverse t2 = Node (tree_reverse r) v (tree_reverse l)" by simp
    with `tree_reverse t2 = Leaf` show ?thesis by simp
  qed
next
  case (Node l1 v1 r1)
  then obtain t2_l t2_v t2_r where t2_eq: "t2 = Node t2_l t2_v t2_r \<or> t2 = Leaf"
    by (cases t2) auto
  then show ?case
  proof
    assume "t2 = Leaf"
    with Node.prems have "tree_reverse t2 = Leaf" by simp
    then have "Node (tree_reverse r1) v1 (tree_reverse l1) = Leaf" using Node.prems by simp
    thus ?thesis by simp
  next
    assume t2_is_node: "t2 = Node t2_l t2_v t2_r"
    with Node.prems have eq_nodes: "Node (tree_reverse r1) v1 (tree_reverse l1) = Node (tree_reverse t2_r) t2_v (tree_reverse t2_l)" by simp
    then have eq_vals: "v1 = t2_v" and eq_left: "tree_reverse l1 = tree_reverse t2_l" and eq_right: "tree_reverse r1 = tree_reverse t2_r" by auto
    from Node.IH[OF eq_right] have "r1 = t2_r" by blast
    from Node.IH[OF eq_left] have "l1 = t2_l" by blast
    with `v1 = t2_v` `r1 = t2_r` t2_is_node show ?thesis by simp
  qed
qed

end

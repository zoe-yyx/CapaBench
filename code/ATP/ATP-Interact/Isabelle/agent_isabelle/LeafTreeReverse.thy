theory LeafTreeReverse
  imports Main
begin

datatype tree = Leaf | Node tree int tree

fun tree_reverse :: "tree \<Rightarrow> tree" where
"tree_reverse Leaf = Leaf" |
"tree_reverse (Node l v r) = Node (tree_reverse r) v (tree_reverse l)"

lemma Leaf_tree_reverse: "tree_reverse Leaf = Leaf"
proof -
  show ?thesis by simp
qed

end

theory Treeexample3bSize
  imports Main
begin

datatype tree = Leaf | Node tree int tree

definition tree_example2b :: tree where
"tree_example2b = Node (Node Leaf 9 Leaf) 100 (Node Leaf 8 Leaf)"

definition tree_example3b :: tree where
"tree_example3b = Node tree_example2b 5 (Node Leaf 3 Leaf)"

fun tree_size :: "tree \<Rightarrow> int" where
"tree_size Leaf = 0" |
"tree_size (Node l v r) = tree_size l + tree_size r + 1"

lemma treeexample3b_size: "tree_size tree_example3b = 5"
proof -
  show ?thesis
    unfolding tree_example3b_def tree_example2b_def
    by simp
qed

end

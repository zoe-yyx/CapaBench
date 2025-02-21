theory TreeExample2aHeight
  imports Main
begin

datatype tree = Leaf | Node tree int tree

definition tree_example2a :: tree where
"tree_example2a = Node (Node Leaf 8 Leaf) 100 (Node Leaf 9 Leaf)"

fun tree_height :: "tree \<Rightarrow> int" where
"tree_height Leaf = 0" |
"tree_height (Node l v r) = max (tree_height l) (tree_height r) + 1"

lemma tree_example2a_height: "tree_height tree_example2a = 2"
proof -
  show ?thesis
    unfolding tree_example2a_def
    by simp
qed

end

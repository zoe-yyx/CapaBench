theory TreeExample3TreeReverse
  imports Main
begin

datatype tree = Leaf | Node tree int tree

definition tree_example2a :: tree where
"tree_example2a = Node (Node Leaf 8 Leaf) 100 (Node Leaf 9 Leaf)"

definition tree_example2b :: tree where
"tree_example2b = Node (Node Leaf 9 Leaf) 100 (Node Leaf 8 Leaf)"

definition tree_example3a :: tree where
"tree_example3a = Node (Node Leaf 3 Leaf) 5 tree_example2a"

definition tree_example3b :: tree where
"tree_example3b = Node tree_example2b 5 (Node Leaf 3 Leaf)"

fun tree_reverse :: "tree \<Rightarrow> tree" where
"tree_reverse Leaf = Leaf" |
"tree_reverse (Node l v r) = Node (tree_reverse r) v (tree_reverse l)"

lemma tree_example3_tree_reverse: "tree_reverse tree_example3a = tree_example3b"
proof -
  show ?thesis
    unfolding tree_example3a_def tree_example3b_def tree_example2a_def tree_example2b_def
    by simp
qed

end

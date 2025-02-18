theory TreeExample0TreeReverse
  imports Main
begin

datatype tree = Leaf | Node tree int tree

definition tree_example0 :: tree where
"tree_example0 = Node Leaf 1 Leaf"

fun tree_reverse :: "tree \<Rightarrow> tree" where
"tree_reverse Leaf = Leaf" |
"tree_reverse (Node l v r) = Node (tree_reverse r) v (tree_reverse l)"

lemma tree_example0_tree_reverse: "tree_reverse tree_example0 = tree_example0"
proof -
  show ?thesis
    unfolding tree_example0_def
    by simp
qed

end

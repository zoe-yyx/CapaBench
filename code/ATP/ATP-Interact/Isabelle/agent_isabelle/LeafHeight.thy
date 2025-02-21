theory LeafHeight
  imports Main
begin

datatype tree = Leaf | Node tree int tree

fun tree_height :: "tree \<Rightarrow> int" where
"tree_height Leaf = 0" |
"tree_height (Node l v r) = max (tree_height l) (tree_height r) + 1"

lemma Leaf_height: "tree_height Leaf = 0"
proof -
  show ?thesis by simp
qed

end

theory ReverseHeight
  imports Main
begin

datatype tree =
  Leaf
| Node tree int tree

fun tree_reverse :: "tree \<Rightarrow> tree" where
  "tree_reverse Leaf = Leaf"
| "tree_reverse (Node l v r) = Node (tree_reverse r) v (tree_reverse l)"

fun tree_height :: "tree \<Rightarrow> int" where
  "tree_height Leaf = 0"
| "tree_height (Node l v r) = max (tree_height l) (tree_height r) + 1"

lemma reverse_height: "tree_height (tree_reverse t) = tree_height t"
proof (induction t)
  case Leaf
  then show ?case by simp
next
  case (Node l v r)
  then show ?case by (simp add: Node.IH max.commute)
qed

end

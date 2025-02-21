theory ReverseResultLeaf
  imports Main
begin

datatype tree = Leaf | Node tree int tree

fun tree_reverse :: "tree \<Rightarrow> tree" where
  "tree_reverse Leaf = Leaf"
| "tree_reverse (Node l v r) = Node (tree_reverse r) v (tree_reverse l)"

lemma reverse_result_Leaf:
  assumes "tree_reverse t = Leaf"
  shows "t = Leaf"
proof (cases t)
  case Leaf
  then show ?thesis by simp
next
  case (Node l v r)
  then have "tree_reverse t = Node (tree_reverse r) v (tree_reverse l)"
    by simp
  with assms have "Node (tree_reverse r) v (tree_reverse l) = Leaf"
    by simp
  then have False
    by simp  \<comment> \<open>Let 'simp' automatically use the distinctness of constructors\<close>
  then show ?thesis
    by simp
qed


end

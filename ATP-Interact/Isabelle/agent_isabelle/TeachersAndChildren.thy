theory TeachersAndChildren
  imports Main
begin

lemma teachers_and_children:
  fixes MT FT MC FC :: int
  assumes "MT > 0"
    and "FT > 0"
    and "MC > 0"
    and "FC > 0"
    and "MT + FT + MC + FC = 16"
    and "MC + FC > MT + FT"
    and "FT > FC"
    and "FC > MC"
    and "MC > MT"
  shows "MT = 1"
proof -
  from assms have "MT = 1"
    by arith
  thus ?thesis.
qed

end

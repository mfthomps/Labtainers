/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package GoalsUI;

import GoalsUI.ToolTipHandlers.ToolTipWrapper;
import java.util.ArrayList;
import java.util.Arrays;


/**
 *
 * @author Dan
 */
public class ParamReferenceStorage {
    
    public static final ToolTipWrapper[] GoalType_ITEMS = new ToolTipWrapper[] {
        //0
        new ToolTipWrapper("matchany", "<html>Results from all timestamped sets are evaluated.<br>" +
                                       "If the answertag names a result, then both that<br>" +
                                       "result and the resulttag must occur in the same<br>" +
                                       "timestamped set. The ’matchany’ goals are treated<br>" +
                                       "as a set of values, each timestamped based on the<br>" +
                                       "timestamp of the reference resulttag.</html>"),
        // 1
        new ToolTipWrapper("matchlast", "<html>only results from the latest timestamped set are<br>" +
                                        "evaluated.</html>"),
        // 2
        new ToolTipWrapper("matchacross", "<html>The resulttag and answertag name results. The<br>" +
                                          "operator is applied against values in different<br>" +
                                          "timestamped sets. For example, a \"string_diff\"<br>" +
                                          "operator would require the named results to have<br>" +
                                          "at least two distinct values in different<br>" +
                                          "timestamped sets.</html>"), 
        // 3
        new ToolTipWrapper("boolean", "<html>The goal value is computed from a boolean expression<br>" +
                                      "consisting of goal_id’s and boolean operators, (\"and\",<br>" +
                                      "\"or\", \"and_not\", \"or_not\", and \"not\"), and parenthisis<br>" +
                                      "for precedence. The goal_id’s must be from goals defined<br>" +
                                      "earlier in the goals.config file, or boolean results<br>" +
                                      "from results.config. The goal evalutes to<br>" +
                                      "TRUE if the boolen expression evaluates to TRUE for any<br>" +
                                      "of the timestamped sets of goal_ids, (see the ’matchany’<br>" +
                                      "discussion above). The goal_id’s cannot include any<br>" +
                                      "\"matchacross\" goals. NOTE: evaluation is within<br>" +
                                      "timestamped sets. If you want to evaluate across<br>" +
                                      "timestamps, use the count_greater_operator below.</html>"), 
        // 4
        new ToolTipWrapper("count_greater", "<html>The goal is TRUE if the count of TRUE subgoals in the<br>" +
                                            "list exceeds the given value. The subgoals are<br>" +
                                            "summed across all timestamps. The subgoal list is<br>" +
                                            "comma-separated within parenthesis.</html>"), 
        // 5
        new ToolTipWrapper("time_before", "<html>Both goal1 and goal2 must be goal_ids from previous<br>" +
                                          "matchany, or boolean values from results.config<br>" +
                                          "A timestamped goal is created for each goal2<br>" +
                                          "timestamped instance whose timestamp is proceeded<br>" +
                                          "by a goal1 timestamped instance. The goal for that<br>" +
                                          "timestamp will be TRUE if the goal2<br>" +
                                          "instance is TRUE, and at least one of the goal1<br>" +
                                          "instances is TRUE. These timestamped goals can<br>" +
                                          "then be evaluated within boolean goals.</html>"), 
        // 6
        new ToolTipWrapper("time_during", "<html>Both goal1 and goal2 must be goal_ids from previous<br>" +
                                          "matchany goal types, or boolean values from<br>" +
                                          "results.config. Timestamps include a start and end<br>" +
                                          "time, reflecting when the program starts and when it<br>" +
                                          "terminates. A timestamped goal is created for each<br>" +
                                          "goal2 range that encompasses a goal1 timestamp.<br>" +
                                          "The goal for that timestamp will be TRUE if the<br>" +
                                          "goal2 instance is TRUE, and at least one goal1 instance<br>" +
                                          "is TRUE. These timestamped goals can then be<br>" +
                                          "evaluated within boolean goals.</html>"), 
        // 7
        new ToolTipWrapper("time_not_during", "<html>Similar to time_during, but timestamped goals are<br>" +
                                              "always created for each goal2. Each such goal is True<br>" +
                                              "unless one or more goal1 times occur within a True goal2<br>" +
                                              "range.</html>"), 
        // 8
        new ToolTipWrapper("execute", "<html>The <operator> is treated as a file name of a script to<br>" +
                                      "execute, with the resulttag and answertag passed to the<br>" +
                                      "script as arguments. The resulttag is expected to be<br>" +
                                      "one of the symbolic names defined in the results.config<br>" +
                                      "file, while the answertag is expected to be a literal<br>" +
                                      "value or the symbolic name in the parameters.config file<br>" +
                                      "Note: the answertag cannot be a symbolic name from<br>" +
                                      "results.config</html>"),
        // 9
        new ToolTipWrapper("count_value", "<html>If the remainder of the line only includes a resulttag,<br>" +
                                          "then the goal value is assigned the quanity of<br>" +
                                          "timestamped files containing the given resulttag.<br>" +
                                          "Otherwise the goal value is assigned the<br>" +
                                          "quantity of timestamped files having results<br>" +
                                          "that satisfy the given operator and arguments.</html>"), 
        // 10    
        new ToolTipWrapper("count_matches", "<html>If the remainder of the line only includes a resulttag,<br>" +
                                            "then the goal value is assigned the quanity of<br>" +
                                            "timestamped files containing the given resulttag.<br>" +
                                            "Otherwise the goal value is assigned the<br>" +
                                            "quantity of timestamped files having results<br>" +
                                            "that satisfy the given operator and arguments.</html>"), 
        // 11        
        new ToolTipWrapper("value", "<html>The goal value is assigned the given resulttag value from<br>" +
                                    "the most recent timestamped file that contains the resulttag.</html>"),
            
        // 12
        new ToolTipWrapper("matchExpression", "<html>The resultTag is an arithmetic expression</html>")};

    
    public static final ToolTipWrapper[] Operator_ITEMS = new ToolTipWrapper[] {
        // 0
        new ToolTipWrapper("string_equal", "<html>The strings derived from answertag and resulttag<br>" +
                                           "are equal.</html>"), 
        // 1
        new ToolTipWrapper("string_diff", "<html>The line_id is an integer line number<br>" +
                                   "(starting at one). Use of this to identify<br>" +
                                   "lines is discouraged since minor lab changes<br>" +
                                   "might alter the count.</html>"), 
        // 2
        new ToolTipWrapper("string_start", "<html>the line_id is a string. This names the<br>" +
                                         "first occurrence of a line that starts with<br>" +
                                         "this string.</html>" ), 
        // 3
        new ToolTipWrapper("string_end", "<html>The line_id is a string. This names the<br>" + 
                                         "first occurrence of a line that contains the<br>" +
                                         "string.</html>" ), 
        // 4
        new ToolTipWrapper("string_contains", "<html>The line_id is a regular expression. This names the<br>" + 
                                    "first occurrence of a line that matches the regular<br>" +
                                    "expression. Also see the \"GROUP\" field_type.</html>" ), 
        
        // 5
        new ToolTipWrapper("integer_equal", "<html>The line_id is a regular expression. This names the<br>" + 
                                    "first occurrence of a line that matches the regular<br>" +
                                    "expression. Also see the \"GROUP\" field_type.</html>" ), 
        
        // 6
        new ToolTipWrapper("integer_greater", "<html>The line_id is a regular expression. This names the<br>" + 
                                    "first occurrence of a line that matches the regular<br>" +
                                    "expression. Also see the \"GROUP\" field_type.</html>" ), 
        
        // 7
        new ToolTipWrapper("integer_lessthan", "<html>The line_id is a regular expression. This names the<br>" + 
                                    "first occurrence of a line that matches the regular<br>" +
                                    "expression. Also see the \"GROUP\" field_type.</html>" )}; 
                                    
    
        //Answer Types
        public static final String[] answerTypes = new String[] {
                "Literal",
                "Result Tag",
                "Parameter",
                "Parameter ASCII"  
        };
        
        //Boolean Result Types
        public static final ArrayList<String> booleanResultTypes = new ArrayList<String>(Arrays.asList(
                "CONTAINS",
                "FILE_REGEX",
                "LOG_TS",
                "FILE_REGEX_TS",
                "LOG_RANGE",
                "TIME_DELIM"
        ));
    
        //Input format 1: [operator : resultTag : answerTag]
        public static final ArrayList<String> opInput = new ArrayList<String>(Arrays.asList(
                "matchany",
                "matchlast",
                "matchacross",
                "count_matches"   
        ));
        
        //Input format 2: [goal1 : goal2]
        public static final ArrayList<String> goalInput = new ArrayList<String>(Arrays.asList(
                "time_before",
                "time_during",
                "time_not_during"       
        ));
        
        //Input format 2: [resultTag]
        public static final ArrayList<String> resultTagInput = new ArrayList<String>(Arrays.asList(
                "count_value",
                "value"       
        ));
        
        
}

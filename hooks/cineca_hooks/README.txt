This is a very poor README.

infile_examples/:  contains file that can be used to test hooks 
    - pbs_python --hook -i <file_representing_a_PBS_event> <hook>
    - pbs_python --hook -i  infile_examples/hook_execjob_begin_cgroups_428.in
      aborghesi_hook_noTmpDirs_TEST.py

testing_hooks/:    I honestly don't remember its content..


aborghesi_hook_noTmpDirs.py:  Current version of Galileo hook (well not current
    since Galileo has been dismissed..)

aborghesi_hook_noTmpDirs_TEST.py:  Current version of Galileo hook version to
    be used for testing (not directly attachable to PBS)

aborghesi_hook.py:  Old version of Galileo hook that used a series of useless
    temporary directories

# *_DELIMITER are used within preexec / precmd zsh hooks to so that
# we can parse out command information for logging commands, their outputs
# and their statuses.
START_COMMAND_DELIMITER = "71DbDeuXGpbEn8KO93V4kH56xr992Zu3RoUAW0lWesqPWCFff9PVr1RE"
START_OUTPUT_DELIMITER = "YJipyPN4Quh41VbKKHoYqS6bUzw8d0soTo8W61jeBTQUm9F4IRZvQoqg"
END_COMMAND_DELIMITER = "FwCsfKV6Xfg7PbUJD9sJfZWRBgfAG9uQBj4BBx6uWnss5k2HA3VXtuwb"

# The default zshrc file that will be used by our zsh terminal.
# This includes output delimiters
zshrc = """
autoload -U add-zsh-hook

print_start_output_delimiter() {{
  echo "{START_COMMAND_DELIMITER}"
  # the command
  echo $1
  echo "{START_OUTPUT_DELIMITER}"
}}

print_end_output_delimiter() {{
  # the command exit code
  echo $?
  echo "{END_COMMAND_DELIMITER}"
}}
add-zsh-hook preexec print_start_output_delimiter
add-zsh-hook precmd print_end_output_delimiter

""".format(
    START_COMMAND_DELIMITER=START_COMMAND_DELIMITER,
    START_OUTPUT_DELIMITER=START_OUTPUT_DELIMITER,
    END_COMMAND_DELIMITER=END_COMMAND_DELIMITER,
)


# write_zshrc will create a .zshrc file within /tmp/.zshrc
# Use /tmp/ rather than ~ because WT does not write to same
# relative paths as the user.
# When instatiating each zsh, we can use ZDOTDIR=/tmp zsh
# so that it uses this .zshrc file.
def write_zshrc() -> None:
    zshrc_file = open("/tmp/.zshrc", "w")
    zshrc_file.write(zshrc)
    zshrc_file.close()

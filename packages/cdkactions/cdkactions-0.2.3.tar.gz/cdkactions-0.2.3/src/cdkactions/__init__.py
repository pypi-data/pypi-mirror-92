"""
# cdkactions

See the [main README](https://github.com/ArmaanT/cdkactions/) for an overview of cdkactions.

See the [API reference](https://github.com/ArmaanT/cdkactions/blob/master/packages/cdkactions/API.md) for detailed information about the cdkactions constructs.

## License

This project is distributed under the [Apache License, Version 2.0](./LICENSE).
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import constructs


class App(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdkactions.App"):
    """Represents a cdkactions application."""

    def __init__(
        self,
        *,
        create_validate_workflow: typing.Optional[builtins.bool] = None,
        outdir: typing.Optional[builtins.str] = None,
        push_updated_manifests: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Defines a cdkaction app.

        :param create_validate_workflow: Create a validation workflow to ensure cdkactions manifests are up to date. Default: - true
        :param outdir: The directory to synthesize GitHub Action manifests in. Default: - "../workflows"
        :param push_updated_manifests: Push updated manifests if they are out of date. Only used if ``createValidateWorkflow`` is true. Default: - false
        """
        options = AppProps(
            create_validate_workflow=create_validate_workflow,
            outdir=outdir,
            push_updated_manifests=push_updated_manifests,
        )

        jsii.create(App, self, [options])

    @jsii.member(jsii_name="synth")
    def synth(self) -> None:
        """Synthesizes all manifests into the output directory."""
        return jsii.invoke(self, "synth", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        """The directory to synthesize GitHub Action manifests in."""
        return jsii.get(self, "outdir")


@jsii.data_type(
    jsii_type="cdkactions.AppProps",
    jsii_struct_bases=[],
    name_mapping={
        "create_validate_workflow": "createValidateWorkflow",
        "outdir": "outdir",
        "push_updated_manifests": "pushUpdatedManifests",
    },
)
class AppProps:
    def __init__(
        self,
        *,
        create_validate_workflow: typing.Optional[builtins.bool] = None,
        outdir: typing.Optional[builtins.str] = None,
        push_updated_manifests: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Configuration for a cdkactions app.

        :param create_validate_workflow: Create a validation workflow to ensure cdkactions manifests are up to date. Default: - true
        :param outdir: The directory to synthesize GitHub Action manifests in. Default: - "../workflows"
        :param push_updated_manifests: Push updated manifests if they are out of date. Only used if ``createValidateWorkflow`` is true. Default: - false
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if create_validate_workflow is not None:
            self._values["create_validate_workflow"] = create_validate_workflow
        if outdir is not None:
            self._values["outdir"] = outdir
        if push_updated_manifests is not None:
            self._values["push_updated_manifests"] = push_updated_manifests

    @builtins.property
    def create_validate_workflow(self) -> typing.Optional[builtins.bool]:
        """Create a validation workflow to ensure cdkactions manifests are up to date.

        :default: - true
        """
        result = self._values.get("create_validate_workflow")
        return result

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        """The directory to synthesize GitHub Action manifests in.

        :default: - "../workflows"
        """
        result = self._values.get("outdir")
        return result

    @builtins.property
    def push_updated_manifests(self) -> typing.Optional[builtins.bool]:
        """Push updated manifests if they are out of date.

        Only used if ``createValidateWorkflow`` is true.

        :default: - false
        """
        result = self._values.get("push_updated_manifests")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.CDKActionsProps",
    jsii_struct_bases=[],
    name_mapping={"push_updated_manifests": "pushUpdatedManifests"},
)
class CDKActionsProps:
    def __init__(
        self,
        *,
        push_updated_manifests: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Configuration for a CDKActionsStack instance.

        :param push_updated_manifests: Push updated manifests if they are out of date. Default: - false
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if push_updated_manifests is not None:
            self._values["push_updated_manifests"] = push_updated_manifests

    @builtins.property
    def push_updated_manifests(self) -> typing.Optional[builtins.bool]:
        """Push updated manifests if they are out of date.

        :default: - false
        """
        result = self._values.get("push_updated_manifests")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CDKActionsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.CheckRunTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class CheckRunTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the CheckRun event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckRunTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.CheckSuiteTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class CheckSuiteTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the CheckSuite event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckSuiteTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.CredentialsProps",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class CredentialsProps:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        """Credentials to connect to a Docker registry with.

        :param password: Password to connect with.
        :param username: Username to connect with.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        """Password to connect with."""
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return result

    @builtins.property
    def username(self) -> builtins.str:
        """Username to connect with."""
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CredentialsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.DefaultsProps",
    jsii_struct_bases=[],
    name_mapping={"run": "run"},
)
class DefaultsProps:
    def __init__(self, *, run: typing.Optional["RunProps"] = None) -> None:
        """A defaults configuration block.

        :param run: A RunProps block.
        """
        if isinstance(run, dict):
            run = RunProps(**run)
        self._values: typing.Dict[str, typing.Any] = {}
        if run is not None:
            self._values["run"] = run

    @builtins.property
    def run(self) -> typing.Optional["RunProps"]:
        """A RunProps block."""
        result = self._values.get("run")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DefaultsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.DockerProps",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "credentials": "credentials",
        "env": "env",
        "options": "options",
        "ports": "ports",
        "volumes": "volumes",
    },
)
class DockerProps:
    def __init__(
        self,
        *,
        image: builtins.str,
        credentials: typing.Optional[CredentialsProps] = None,
        env: typing.Optional["StringMap"] = None,
        options: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.List[builtins.str]] = None,
        volumes: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Generic Docker configuration.

        :param image: Image to use.
        :param credentials: Credential configuration.
        :param env: Additional environment variables.
        :param options: Additional Docker options.
        :param ports: Ports to map.
        :param volumes: Volumes to map.
        """
        if isinstance(credentials, dict):
            credentials = CredentialsProps(**credentials)
        if isinstance(env, dict):
            env = StringMap(**env)
        self._values: typing.Dict[str, typing.Any] = {
            "image": image,
        }
        if credentials is not None:
            self._values["credentials"] = credentials
        if env is not None:
            self._values["env"] = env
        if options is not None:
            self._values["options"] = options
        if ports is not None:
            self._values["ports"] = ports
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def image(self) -> builtins.str:
        """Image to use."""
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return result

    @builtins.property
    def credentials(self) -> typing.Optional[CredentialsProps]:
        """Credential configuration."""
        result = self._values.get("credentials")
        return result

    @builtins.property
    def env(self) -> typing.Optional["StringMap"]:
        """Additional environment variables."""
        result = self._values.get("env")
        return result

    @builtins.property
    def options(self) -> typing.Optional[builtins.str]:
        """Additional Docker options."""
        result = self._values.get("options")
        return result

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[builtins.str]]:
        """Ports to map."""
        result = self._values.get("ports")
        return result

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[builtins.str]]:
        """Volumes to map."""
        result = self._values.get("volumes")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.EventMap",
    jsii_struct_bases=[],
    name_mapping={
        "check_run": "checkRun",
        "check_suite": "checkSuite",
        "issue_comment": "issueComment",
        "issues": "issues",
        "label": "label",
        "milestone": "milestone",
        "project": "project",
        "project_card": "projectCard",
        "project_column": "projectColumn",
        "pull_request": "pullRequest",
        "pull_request_review": "pullRequestReview",
        "pull_request_review_comment": "pullRequestReviewComment",
        "pull_request_target": "pullRequestTarget",
        "push": "push",
        "registry_package": "registryPackage",
        "release": "release",
        "watch": "watch",
    },
)
class EventMap:
    def __init__(
        self,
        *,
        check_run: typing.Optional[CheckRunTypes] = None,
        check_suite: typing.Optional[CheckSuiteTypes] = None,
        issue_comment: typing.Optional["IssueCommentTypes"] = None,
        issues: typing.Optional["IssuesTypes"] = None,
        label: typing.Optional["LabelTypes"] = None,
        milestone: typing.Optional["MilestoneTypes"] = None,
        project: typing.Optional["ProjectTypes"] = None,
        project_card: typing.Optional["ProjectCardTypes"] = None,
        project_column: typing.Optional["ProjectColumnTypes"] = None,
        pull_request: typing.Optional["PullRequestTypes"] = None,
        pull_request_review: typing.Optional["PullRequestReviewTypes"] = None,
        pull_request_review_comment: typing.Optional["PullRequestReviewCommentTypes"] = None,
        pull_request_target: typing.Optional["PullRequestTargetTypes"] = None,
        push: typing.Optional["PushTypes"] = None,
        registry_package: typing.Optional["RegistryPackageTypes"] = None,
        release: typing.Optional["ReleaseTypes"] = None,
        watch: typing.Optional["WatchTypes"] = None,
    ) -> None:
        """Events with additional subtypes.

        :param check_run: The checkRun event.
        :param check_suite: The checkSuite event.
        :param issue_comment: The issueComment event.
        :param issues: The issues event.
        :param label: The label event.
        :param milestone: The milestone event.
        :param project: The project event.
        :param project_card: The projectCard event.
        :param project_column: The projectColumn event.
        :param pull_request: The pullRequest event.
        :param pull_request_review: The pullRequestReview event.
        :param pull_request_review_comment: The pullRequestReviewComment event.
        :param pull_request_target: The pullRequestTarget event.
        :param push: The push event.
        :param registry_package: The registryPackage event.
        :param release: The release event.
        :param watch: The watch event.
        """
        if isinstance(check_run, dict):
            check_run = CheckRunTypes(**check_run)
        if isinstance(check_suite, dict):
            check_suite = CheckSuiteTypes(**check_suite)
        if isinstance(issue_comment, dict):
            issue_comment = IssueCommentTypes(**issue_comment)
        if isinstance(issues, dict):
            issues = IssuesTypes(**issues)
        if isinstance(label, dict):
            label = LabelTypes(**label)
        if isinstance(milestone, dict):
            milestone = MilestoneTypes(**milestone)
        if isinstance(project, dict):
            project = ProjectTypes(**project)
        if isinstance(project_card, dict):
            project_card = ProjectCardTypes(**project_card)
        if isinstance(project_column, dict):
            project_column = ProjectColumnTypes(**project_column)
        if isinstance(pull_request, dict):
            pull_request = PullRequestTypes(**pull_request)
        if isinstance(pull_request_review, dict):
            pull_request_review = PullRequestReviewTypes(**pull_request_review)
        if isinstance(pull_request_review_comment, dict):
            pull_request_review_comment = PullRequestReviewCommentTypes(**pull_request_review_comment)
        if isinstance(pull_request_target, dict):
            pull_request_target = PullRequestTargetTypes(**pull_request_target)
        if isinstance(push, dict):
            push = PushTypes(**push)
        if isinstance(registry_package, dict):
            registry_package = RegistryPackageTypes(**registry_package)
        if isinstance(release, dict):
            release = ReleaseTypes(**release)
        if isinstance(watch, dict):
            watch = WatchTypes(**watch)
        self._values: typing.Dict[str, typing.Any] = {}
        if check_run is not None:
            self._values["check_run"] = check_run
        if check_suite is not None:
            self._values["check_suite"] = check_suite
        if issue_comment is not None:
            self._values["issue_comment"] = issue_comment
        if issues is not None:
            self._values["issues"] = issues
        if label is not None:
            self._values["label"] = label
        if milestone is not None:
            self._values["milestone"] = milestone
        if project is not None:
            self._values["project"] = project
        if project_card is not None:
            self._values["project_card"] = project_card
        if project_column is not None:
            self._values["project_column"] = project_column
        if pull_request is not None:
            self._values["pull_request"] = pull_request
        if pull_request_review is not None:
            self._values["pull_request_review"] = pull_request_review
        if pull_request_review_comment is not None:
            self._values["pull_request_review_comment"] = pull_request_review_comment
        if pull_request_target is not None:
            self._values["pull_request_target"] = pull_request_target
        if push is not None:
            self._values["push"] = push
        if registry_package is not None:
            self._values["registry_package"] = registry_package
        if release is not None:
            self._values["release"] = release
        if watch is not None:
            self._values["watch"] = watch

    @builtins.property
    def check_run(self) -> typing.Optional[CheckRunTypes]:
        """The checkRun event."""
        result = self._values.get("check_run")
        return result

    @builtins.property
    def check_suite(self) -> typing.Optional[CheckSuiteTypes]:
        """The checkSuite event."""
        result = self._values.get("check_suite")
        return result

    @builtins.property
    def issue_comment(self) -> typing.Optional["IssueCommentTypes"]:
        """The issueComment event."""
        result = self._values.get("issue_comment")
        return result

    @builtins.property
    def issues(self) -> typing.Optional["IssuesTypes"]:
        """The issues event."""
        result = self._values.get("issues")
        return result

    @builtins.property
    def label(self) -> typing.Optional["LabelTypes"]:
        """The label event."""
        result = self._values.get("label")
        return result

    @builtins.property
    def milestone(self) -> typing.Optional["MilestoneTypes"]:
        """The milestone event."""
        result = self._values.get("milestone")
        return result

    @builtins.property
    def project(self) -> typing.Optional["ProjectTypes"]:
        """The project event."""
        result = self._values.get("project")
        return result

    @builtins.property
    def project_card(self) -> typing.Optional["ProjectCardTypes"]:
        """The projectCard event."""
        result = self._values.get("project_card")
        return result

    @builtins.property
    def project_column(self) -> typing.Optional["ProjectColumnTypes"]:
        """The projectColumn event."""
        result = self._values.get("project_column")
        return result

    @builtins.property
    def pull_request(self) -> typing.Optional["PullRequestTypes"]:
        """The pullRequest event."""
        result = self._values.get("pull_request")
        return result

    @builtins.property
    def pull_request_review(self) -> typing.Optional["PullRequestReviewTypes"]:
        """The pullRequestReview event."""
        result = self._values.get("pull_request_review")
        return result

    @builtins.property
    def pull_request_review_comment(
        self,
    ) -> typing.Optional["PullRequestReviewCommentTypes"]:
        """The pullRequestReviewComment event."""
        result = self._values.get("pull_request_review_comment")
        return result

    @builtins.property
    def pull_request_target(self) -> typing.Optional["PullRequestTargetTypes"]:
        """The pullRequestTarget event."""
        result = self._values.get("pull_request_target")
        return result

    @builtins.property
    def push(self) -> typing.Optional["PushTypes"]:
        """The push event."""
        result = self._values.get("push")
        return result

    @builtins.property
    def registry_package(self) -> typing.Optional["RegistryPackageTypes"]:
        """The registryPackage event."""
        result = self._values.get("registry_package")
        return result

    @builtins.property
    def release(self) -> typing.Optional["ReleaseTypes"]:
        """The release event."""
        result = self._values.get("release")
        return result

    @builtins.property
    def watch(self) -> typing.Optional["WatchTypes"]:
        """The watch event."""
        result = self._values.get("watch")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.IssueCommentTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class IssueCommentTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the IssueComment event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssueCommentTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.IssuesTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class IssuesTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the Issues event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssuesTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Job(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdkactions.Job"):
    """Represents a GH Actions job."""

    def __init__(
        self,
        scope: "Workflow",
        id: builtins.str,
        *,
        runs_on: builtins.str,
        steps: typing.List["StepsProps"],
        container: typing.Optional[DockerProps] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[DefaultsProps] = None,
        env: typing.Optional["StringMap"] = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]] = None,
        outputs: typing.Optional["StringMap"] = None,
        services: typing.Optional[typing.Mapping[builtins.str, DockerProps]] = None,
        strategy: typing.Optional["StrategyProps"] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Defines a GitHub Actions job.

        :param scope: Workflow to run within.
        :param id: A unique identifier.
        :param runs_on: The type of machine to run on.
        :param steps: A list of steps to run.
        :param container: A container to run the job in.
        :param continue_on_error: Continue workflow if job fails.
        :param defaults: A map of default settings to apply to all steps in this job.
        :param env: A map of environment variables to provide to the job.
        :param if_: When to run this job.
        :param name: Displayed name of the job.
        :param needs: A job or list of jobs that must successfully complete before running this one.
        :param outputs: A map of outputs for this job.
        :param services: Additional Docker services provided to the job.
        :param strategy: A strategy configuration block.
        :param timeout_minutes: Maximum time before killing the job.
        """
        config = JobProps(
            runs_on=runs_on,
            steps=steps,
            container=container,
            continue_on_error=continue_on_error,
            defaults=defaults,
            env=env,
            if_=if_,
            name=name,
            needs=needs,
            outputs=outputs,
            services=services,
            strategy=strategy,
            timeout_minutes=timeout_minutes,
        )

        jsii.create(Job, self, [scope, id, config])

    @jsii.member(jsii_name="toGHAction")
    def to_gh_action(self) -> typing.Any:
        """Converts the job's configuration into a format that is GitHub Actions compatible."""
        return jsii.invoke(self, "toGHAction", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        """A unique identifier."""
        return jsii.get(self, "id")


@jsii.data_type(
    jsii_type="cdkactions.JobProps",
    jsii_struct_bases=[],
    name_mapping={
        "runs_on": "runsOn",
        "steps": "steps",
        "container": "container",
        "continue_on_error": "continueOnError",
        "defaults": "defaults",
        "env": "env",
        "if_": "if",
        "name": "name",
        "needs": "needs",
        "outputs": "outputs",
        "services": "services",
        "strategy": "strategy",
        "timeout_minutes": "timeoutMinutes",
    },
)
class JobProps:
    def __init__(
        self,
        *,
        runs_on: builtins.str,
        steps: typing.List["StepsProps"],
        container: typing.Optional[DockerProps] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[DefaultsProps] = None,
        env: typing.Optional["StringMap"] = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]] = None,
        outputs: typing.Optional["StringMap"] = None,
        services: typing.Optional[typing.Mapping[builtins.str, DockerProps]] = None,
        strategy: typing.Optional["StrategyProps"] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Configuration for a single GitHub Action job.

        :param runs_on: The type of machine to run on.
        :param steps: A list of steps to run.
        :param container: A container to run the job in.
        :param continue_on_error: Continue workflow if job fails.
        :param defaults: A map of default settings to apply to all steps in this job.
        :param env: A map of environment variables to provide to the job.
        :param if_: When to run this job.
        :param name: Displayed name of the job.
        :param needs: A job or list of jobs that must successfully complete before running this one.
        :param outputs: A map of outputs for this job.
        :param services: Additional Docker services provided to the job.
        :param strategy: A strategy configuration block.
        :param timeout_minutes: Maximum time before killing the job.
        """
        if isinstance(container, dict):
            container = DockerProps(**container)
        if isinstance(defaults, dict):
            defaults = DefaultsProps(**defaults)
        if isinstance(env, dict):
            env = StringMap(**env)
        if isinstance(outputs, dict):
            outputs = StringMap(**outputs)
        if isinstance(strategy, dict):
            strategy = StrategyProps(**strategy)
        self._values: typing.Dict[str, typing.Any] = {
            "runs_on": runs_on,
            "steps": steps,
        }
        if container is not None:
            self._values["container"] = container
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if defaults is not None:
            self._values["defaults"] = defaults
        if env is not None:
            self._values["env"] = env
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if needs is not None:
            self._values["needs"] = needs
        if outputs is not None:
            self._values["outputs"] = outputs
        if services is not None:
            self._values["services"] = services
        if strategy is not None:
            self._values["strategy"] = strategy
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes

    @builtins.property
    def runs_on(self) -> builtins.str:
        """The type of machine to run on."""
        result = self._values.get("runs_on")
        assert result is not None, "Required property 'runs_on' is missing"
        return result

    @builtins.property
    def steps(self) -> typing.List["StepsProps"]:
        """A list of steps to run."""
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return result

    @builtins.property
    def container(self) -> typing.Optional[DockerProps]:
        """A container to run the job in."""
        result = self._values.get("container")
        return result

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        """Continue workflow if job fails."""
        result = self._values.get("continue_on_error")
        return result

    @builtins.property
    def defaults(self) -> typing.Optional[DefaultsProps]:
        """A map of default settings to apply to all steps in this job."""
        result = self._values.get("defaults")
        return result

    @builtins.property
    def env(self) -> typing.Optional["StringMap"]:
        """A map of environment variables to provide to the job."""
        result = self._values.get("env")
        return result

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        """When to run this job."""
        result = self._values.get("if_")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """Displayed name of the job."""
        result = self._values.get("name")
        return result

    @builtins.property
    def needs(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]]:
        """A job or list of jobs that must successfully complete before running this one."""
        result = self._values.get("needs")
        return result

    @builtins.property
    def outputs(self) -> typing.Optional["StringMap"]:
        """A map of outputs for this job."""
        result = self._values.get("outputs")
        return result

    @builtins.property
    def services(self) -> typing.Optional[typing.Mapping[builtins.str, DockerProps]]:
        """Additional Docker services provided to the job."""
        result = self._values.get("services")
        return result

    @builtins.property
    def strategy(self) -> typing.Optional["StrategyProps"]:
        """A strategy configuration block."""
        result = self._values.get("strategy")
        return result

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        """Maximum time before killing the job."""
        result = self._values.get("timeout_minutes")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.LabelTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class LabelTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the Label event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabelTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.MilestoneTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class MilestoneTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the Milestone event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MilestoneTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.ProjectCardTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectCardTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the ProjectCard event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectCardTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.ProjectColumnTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectColumnTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the ProjectColumn event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectColumnTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.ProjectTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the ProjectTypes event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.PullRequestReviewCommentTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestReviewCommentTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the PullRequestReviewComment event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestReviewCommentTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.PullRequestReviewTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestReviewTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the PullRequestReview event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestReviewTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.PullRequestTargetTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestTargetTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the PullRequestTarget event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestTargetTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.PushTypes",
    jsii_struct_bases=[],
    name_mapping={
        "branches": "branches",
        "branches_ignore": "branchesIgnore",
        "paths": "paths",
        "paths_ignore": "pathsIgnore",
        "tags": "tags",
        "tags_ignore": "tagsIgnore",
    },
)
class PushTypes:
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.List[builtins.str]] = None,
        branches_ignore: typing.Optional[typing.List[builtins.str]] = None,
        paths: typing.Optional[typing.List[builtins.str]] = None,
        paths_ignore: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[builtins.str]] = None,
        tags_ignore: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Configuration for the Push event.

        :param branches: Branches to trigger the workflow on.
        :param branches_ignore: Branches to ignore when triggering the workflow.
        :param paths: Paths to trigger the workflow on.
        :param paths_ignore: Paths to ignore when triggering the workflow.
        :param tags: Tags to trigger the workflow on.
        :param tags_ignore: Tags to ignore when triggering the workflow.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if branches_ignore is not None:
            self._values["branches_ignore"] = branches_ignore
        if paths is not None:
            self._values["paths"] = paths
        if paths_ignore is not None:
            self._values["paths_ignore"] = paths_ignore
        if tags is not None:
            self._values["tags"] = tags
        if tags_ignore is not None:
            self._values["tags_ignore"] = tags_ignore

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        """Branches to trigger the workflow on."""
        result = self._values.get("branches")
        return result

    @builtins.property
    def branches_ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        """Branches to ignore when triggering the workflow."""
        result = self._values.get("branches_ignore")
        return result

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        """Paths to trigger the workflow on."""
        result = self._values.get("paths")
        return result

    @builtins.property
    def paths_ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        """Paths to ignore when triggering the workflow."""
        result = self._values.get("paths_ignore")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        """Tags to trigger the workflow on."""
        result = self._values.get("tags")
        return result

    @builtins.property
    def tags_ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        """Tags to ignore when triggering the workflow."""
        result = self._values.get("tags_ignore")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PushTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.RegistryPackageTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class RegistryPackageTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the RegistryPackage event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegistryPackageTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.ReleaseTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ReleaseTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the Release event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.RunProps",
    jsii_struct_bases=[],
    name_mapping={"shell": "shell", "working_directory": "workingDirectory"},
)
class RunProps:
    def __init__(
        self,
        *,
        shell: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        """Configuration for a shell environment.

        :param shell: The shell to use.
        :param working_directory: A custom working directory.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if shell is not None:
            self._values["shell"] = shell
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def shell(self) -> typing.Optional[builtins.str]:
        """The shell to use."""
        result = self._values.get("shell")
        return result

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        """A custom working directory."""
        result = self._values.get("working_directory")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.ScheduleEvent",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule"},
)
class ScheduleEvent:
    def __init__(self, *, schedule: typing.Mapping[typing.Any, typing.Any]) -> None:
        """Configuration for the Schedule event.

        :param schedule: A cron schedule to run the workflow on.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "schedule": schedule,
        }

    @builtins.property
    def schedule(self) -> typing.Mapping[typing.Any, typing.Any]:
        """A cron schedule to run the workflow on."""
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleEvent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Stack(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdkactions.Stack",
):
    """Represents a cdkaction stack."""

    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        """Defines a cdkaction stack.

        :param scope: cdkaction app.
        :param id: A unique identifier for this stack.
        """
        jsii.create(Stack, self, [scope, id])

    @jsii.member(jsii_name="onSynthesize")
    def _on_synthesize(self, session: constructs.ISynthesisSession) -> None:
        """A custom ``onSynthesize`` function to generate GH Action manifests.

        :param session: Synthesis session.
        """
        return jsii.invoke(self, "onSynthesize", [session])


@jsii.data_type(
    jsii_type="cdkactions.StepsProps",
    jsii_struct_bases=[RunProps],
    name_mapping={
        "shell": "shell",
        "working_directory": "workingDirectory",
        "continue_on_error": "continueOnError",
        "env": "env",
        "id": "id",
        "if_": "if",
        "name": "name",
        "run": "run",
        "timeout_minutes": "timeoutMinutes",
        "uses": "uses",
        "with_": "with",
    },
)
class StepsProps(RunProps):
    def __init__(
        self,
        *,
        shell: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        env: typing.Optional["StringMap"] = None,
        id: typing.Optional[builtins.str] = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        run: typing.Optional[builtins.str] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
        uses: typing.Optional[builtins.str] = None,
        with_: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool]]] = None,
    ) -> None:
        """Propsuration for a single GitHub Action step.

        :param shell: The shell to use.
        :param working_directory: A custom working directory.
        :param continue_on_error: Continue job if step fails.
        :param env: Additional environment variables.
        :param id: A unique identifier.
        :param if_: When to run this step.
        :param name: A name to display when running this action.
        :param run: Commands to run.
        :param timeout_minutes: Maximum time before killing the step.
        :param uses: Use an external action.
        :param with_: A map of parameters for an external action.
        """
        if isinstance(env, dict):
            env = StringMap(**env)
        self._values: typing.Dict[str, typing.Any] = {}
        if shell is not None:
            self._values["shell"] = shell
        if working_directory is not None:
            self._values["working_directory"] = working_directory
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if env is not None:
            self._values["env"] = env
        if id is not None:
            self._values["id"] = id
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if run is not None:
            self._values["run"] = run
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes
        if uses is not None:
            self._values["uses"] = uses
        if with_ is not None:
            self._values["with_"] = with_

    @builtins.property
    def shell(self) -> typing.Optional[builtins.str]:
        """The shell to use."""
        result = self._values.get("shell")
        return result

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        """A custom working directory."""
        result = self._values.get("working_directory")
        return result

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        """Continue job if step fails."""
        result = self._values.get("continue_on_error")
        return result

    @builtins.property
    def env(self) -> typing.Optional["StringMap"]:
        """Additional environment variables."""
        result = self._values.get("env")
        return result

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        """A unique identifier."""
        result = self._values.get("id")
        return result

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        """When to run this step."""
        result = self._values.get("if_")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """A name to display when running this action."""
        result = self._values.get("name")
        return result

    @builtins.property
    def run(self) -> typing.Optional[builtins.str]:
        """Commands to run."""
        result = self._values.get("run")
        return result

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        """Maximum time before killing the step."""
        result = self._values.get("timeout_minutes")
        return result

    @builtins.property
    def uses(self) -> typing.Optional[builtins.str]:
        """Use an external action."""
        result = self._values.get("uses")
        return result

    @builtins.property
    def with_(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool]]]:
        """A map of parameters for an external action."""
        result = self._values.get("with_")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StepsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.StrategyProps",
    jsii_struct_bases=[],
    name_mapping={
        "fast_fail": "fastFail",
        "matrix": "matrix",
        "max_parallel": "maxParallel",
    },
)
class StrategyProps:
    def __init__(
        self,
        *,
        fast_fail: typing.Optional[builtins.bool] = None,
        matrix: typing.Optional[typing.Mapping[builtins.str, typing.List[typing.Any]]] = None,
        max_parallel: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Strategy configuration block.

        :param fast_fail: Stop jobs when a single job fails.
        :param matrix: A matrix to run jobs on.
        :param max_parallel: Maximum parallel jobs.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if fast_fail is not None:
            self._values["fast_fail"] = fast_fail
        if matrix is not None:
            self._values["matrix"] = matrix
        if max_parallel is not None:
            self._values["max_parallel"] = max_parallel

    @builtins.property
    def fast_fail(self) -> typing.Optional[builtins.bool]:
        """Stop jobs when a single job fails."""
        result = self._values.get("fast_fail")
        return result

    @builtins.property
    def matrix(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[typing.Any]]]:
        """A matrix to run jobs on."""
        result = self._values.get("matrix")
        return result

    @builtins.property
    def max_parallel(self) -> typing.Optional[jsii.Number]:
        """Maximum parallel jobs."""
        result = self._values.get("max_parallel")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StrategyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.StringMap",
    jsii_struct_bases=[],
    name_mapping={},
)
class StringMap:
    def __init__(self) -> None:
        """A generic string to string map."""
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StringMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.WatchTypes",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class WatchTypes:
    def __init__(self, *, types: typing.List[builtins.str]) -> None:
        """Configuration for the Watch event.

        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "types": types,
        }

    @builtins.property
    def types(self) -> typing.List[builtins.str]:
        """Supported types."""
        result = self._values.get("types")
        assert result is not None, "Required property 'types' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Workflow(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdkactions.Workflow",
):
    """Represents a GH Action workflow."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        on: typing.Union[ScheduleEvent, "WorkflowRunEvent", EventMap, builtins.str, typing.List[builtins.str]],
        defaults: typing.Optional[DefaultsProps] = None,
        env: typing.Optional[StringMap] = None,
    ) -> None:
        """Represents a GitHub Actions workflow.

        :param scope: An ActionsStack instance.
        :param id: The name of this workflow.
        :param name: Name of the workflow.
        :param on: When to run this workflow.
        :param defaults: A map of default settings to apply to all steps in this job.
        :param env: A map of environment variables to provide to the job.
        """
        config = WorkflowProps(name=name, on=on, defaults=defaults, env=env)

        jsii.create(Workflow, self, [scope, id, config])

    @jsii.member(jsii_name="toGHAction")
    def to_gh_action(self) -> typing.Any:
        """Converts the workflow's configuration into a format that is GitHub Actions compatible."""
        return jsii.invoke(self, "toGHAction", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="outputFile")
    def output_file(self) -> builtins.str:
        """File to save synthesized workflow manifest in."""
        return jsii.get(self, "outputFile")


@jsii.data_type(
    jsii_type="cdkactions.WorkflowProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "on": "on", "defaults": "defaults", "env": "env"},
)
class WorkflowProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        on: typing.Union[ScheduleEvent, "WorkflowRunEvent", EventMap, builtins.str, typing.List[builtins.str]],
        defaults: typing.Optional[DefaultsProps] = None,
        env: typing.Optional[StringMap] = None,
    ) -> None:
        """Configuration for a single GitHub Action workflow.

        :param name: Name of the workflow.
        :param on: When to run this workflow.
        :param defaults: A map of default settings to apply to all steps in this job.
        :param env: A map of environment variables to provide to the job.
        """
        if isinstance(defaults, dict):
            defaults = DefaultsProps(**defaults)
        if isinstance(env, dict):
            env = StringMap(**env)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "on": on,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if env is not None:
            self._values["env"] = env

    @builtins.property
    def name(self) -> builtins.str:
        """Name of the workflow."""
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def on(
        self,
    ) -> typing.Union[ScheduleEvent, "WorkflowRunEvent", EventMap, builtins.str, typing.List[builtins.str]]:
        """When to run this workflow."""
        result = self._values.get("on")
        assert result is not None, "Required property 'on' is missing"
        return result

    @builtins.property
    def defaults(self) -> typing.Optional[DefaultsProps]:
        """A map of default settings to apply to all steps in this job."""
        result = self._values.get("defaults")
        return result

    @builtins.property
    def env(self) -> typing.Optional[StringMap]:
        """A map of environment variables to provide to the job."""
        result = self._values.get("env")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdkactions.WorkflowRunEvent",
    jsii_struct_bases=[],
    name_mapping={
        "workflows": "workflows",
        "branches": "branches",
        "branches_ignore": "branchesIgnore",
        "types": "types",
    },
)
class WorkflowRunEvent:
    def __init__(
        self,
        *,
        workflows: typing.List[builtins.str],
        branches: typing.Optional[typing.List[builtins.str]] = None,
        branches_ignore: typing.Optional[typing.List[builtins.str]] = None,
        types: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Configuration for the WorkflowRun event.

        :param workflows: A list of workflows to trigger from.
        :param branches: Branches to trigger this workflow on.
        :param branches_ignore: Branches to ignore when triggering this workflow.
        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "workflows": workflows,
        }
        if branches is not None:
            self._values["branches"] = branches
        if branches_ignore is not None:
            self._values["branches_ignore"] = branches_ignore
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def workflows(self) -> typing.List[builtins.str]:
        """A list of workflows to trigger from."""
        result = self._values.get("workflows")
        assert result is not None, "Required property 'workflows' is missing"
        return result

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        """Branches to trigger this workflow on."""
        result = self._values.get("branches")
        return result

    @builtins.property
    def branches_ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        """Branches to ignore when triggering this workflow."""
        result = self._values.get("branches_ignore")
        return result

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        """Supported types."""
        result = self._values.get("types")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowRunEvent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CDKActionsStack(
    Stack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdkactions.CDKActionsStack",
):
    """Provided CDKActions Stack that configures a workflow to validate cdkactions."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        push_updated_manifests: typing.Optional[builtins.bool] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param push_updated_manifests: Push updated manifests if they are out of date. Default: - false
        """
        config = CDKActionsProps(push_updated_manifests=push_updated_manifests)

        jsii.create(CDKActionsStack, self, [scope, id, config])


class CheckoutJob(Job, metaclass=jsii.JSIIMeta, jsii_type="cdkactions.CheckoutJob"):
    """A special Job that includes a checkout step automatically."""

    def __init__(
        self,
        scope: Workflow,
        id: builtins.str,
        *,
        runs_on: builtins.str,
        steps: typing.List[StepsProps],
        container: typing.Optional[DockerProps] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[DefaultsProps] = None,
        env: typing.Optional[StringMap] = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Union[builtins.str, typing.List[builtins.str]]] = None,
        outputs: typing.Optional[StringMap] = None,
        services: typing.Optional[typing.Mapping[builtins.str, DockerProps]] = None,
        strategy: typing.Optional[StrategyProps] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param runs_on: The type of machine to run on.
        :param steps: A list of steps to run.
        :param container: A container to run the job in.
        :param continue_on_error: Continue workflow if job fails.
        :param defaults: A map of default settings to apply to all steps in this job.
        :param env: A map of environment variables to provide to the job.
        :param if_: When to run this job.
        :param name: Displayed name of the job.
        :param needs: A job or list of jobs that must successfully complete before running this one.
        :param outputs: A map of outputs for this job.
        :param services: Additional Docker services provided to the job.
        :param strategy: A strategy configuration block.
        :param timeout_minutes: Maximum time before killing the job.
        """
        config = JobProps(
            runs_on=runs_on,
            steps=steps,
            container=container,
            continue_on_error=continue_on_error,
            defaults=defaults,
            env=env,
            if_=if_,
            name=name,
            needs=needs,
            outputs=outputs,
            services=services,
            strategy=strategy,
            timeout_minutes=timeout_minutes,
        )

        jsii.create(CheckoutJob, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdkactions.PullRequestTypes",
    jsii_struct_bases=[PushTypes],
    name_mapping={
        "branches": "branches",
        "branches_ignore": "branchesIgnore",
        "paths": "paths",
        "paths_ignore": "pathsIgnore",
        "tags": "tags",
        "tags_ignore": "tagsIgnore",
        "types": "types",
    },
)
class PullRequestTypes(PushTypes):
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.List[builtins.str]] = None,
        branches_ignore: typing.Optional[typing.List[builtins.str]] = None,
        paths: typing.Optional[typing.List[builtins.str]] = None,
        paths_ignore: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[builtins.str]] = None,
        tags_ignore: typing.Optional[typing.List[builtins.str]] = None,
        types: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Configuration for the PullRequest event.

        :param branches: Branches to trigger the workflow on.
        :param branches_ignore: Branches to ignore when triggering the workflow.
        :param paths: Paths to trigger the workflow on.
        :param paths_ignore: Paths to ignore when triggering the workflow.
        :param tags: Tags to trigger the workflow on.
        :param tags_ignore: Tags to ignore when triggering the workflow.
        :param types: Supported types.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if branches_ignore is not None:
            self._values["branches_ignore"] = branches_ignore
        if paths is not None:
            self._values["paths"] = paths
        if paths_ignore is not None:
            self._values["paths_ignore"] = paths_ignore
        if tags is not None:
            self._values["tags"] = tags
        if tags_ignore is not None:
            self._values["tags_ignore"] = tags_ignore
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        """Branches to trigger the workflow on."""
        result = self._values.get("branches")
        return result

    @builtins.property
    def branches_ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        """Branches to ignore when triggering the workflow."""
        result = self._values.get("branches_ignore")
        return result

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        """Paths to trigger the workflow on."""
        result = self._values.get("paths")
        return result

    @builtins.property
    def paths_ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        """Paths to ignore when triggering the workflow."""
        result = self._values.get("paths_ignore")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        """Tags to trigger the workflow on."""
        result = self._values.get("tags")
        return result

    @builtins.property
    def tags_ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        """Tags to ignore when triggering the workflow."""
        result = self._values.get("tags_ignore")
        return result

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        """Supported types."""
        result = self._values.get("types")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "App",
    "AppProps",
    "CDKActionsProps",
    "CDKActionsStack",
    "CheckRunTypes",
    "CheckSuiteTypes",
    "CheckoutJob",
    "CredentialsProps",
    "DefaultsProps",
    "DockerProps",
    "EventMap",
    "IssueCommentTypes",
    "IssuesTypes",
    "Job",
    "JobProps",
    "LabelTypes",
    "MilestoneTypes",
    "ProjectCardTypes",
    "ProjectColumnTypes",
    "ProjectTypes",
    "PullRequestReviewCommentTypes",
    "PullRequestReviewTypes",
    "PullRequestTargetTypes",
    "PullRequestTypes",
    "PushTypes",
    "RegistryPackageTypes",
    "ReleaseTypes",
    "RunProps",
    "ScheduleEvent",
    "Stack",
    "StepsProps",
    "StrategyProps",
    "StringMap",
    "WatchTypes",
    "Workflow",
    "WorkflowProps",
    "WorkflowRunEvent",
]

publication.publish()

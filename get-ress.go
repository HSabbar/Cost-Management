package main

import (
	"fmt"
    "os"
    "strings"

	"context"

	"github.com/Azure/azure-sdk-for-go/services/network/mgmt/2017-09-01/network"

	"github.com/Azure/go-autorest/autorest/azure/auth"
	"github.com/Azure/go-autorest/autorest/to"
)

func main() {
	// create a VirtualNetworks client
	vnetClient := network.NewVirtualNetworksClient(os.Getenv("AZURE_SUBSCRIPTION_ID"))

	// create an authorizer from env vars or Azure Managed Service Idenity
	authorizer, err := auth.NewAuthorizerFromEnvironment()
	if err == nil {
		vnetClient.Authorizer = authorizer
	}

}
